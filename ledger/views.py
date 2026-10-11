import json
from decimal import Decimal
from datetime import date, timedelta
from calendar import monthrange

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Q

from .models import Client, LedgerEntry
from .forms import ClientForm, LedgerEntryForm


staff_only = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='/login/',
)


def _month_bounds(reference, offset):
    """Return (first_day, last_day) of month offset months before reference."""
    year = reference.year
    month = reference.month - offset
    while month <= 0:
        month += 12
        year -= 1
    first = date(year, month, 1)
    last_day = monthrange(year, month)[1]
    last = date(year, month, last_day)
    return first, last


# =====================================================================
# CLIENT LIST
# =====================================================================

@login_required
@staff_only
def client_list(request):
    clients = Client.objects.all().order_by('name')

    total_outstanding = Decimal('0.00')
    for c in clients:
        total_outstanding += c.outstanding()

    context = {
        'clients': clients,
        'total_clients': clients.count(),
        'total_outstanding': total_outstanding,
    }
    return render(request, 'ledger/client_list.html', context)


# =====================================================================
# CLIENT LEDGER — Excel-style with summary breakdown
# =====================================================================

@login_required
@staff_only
def client_ledger(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    entries = client.entries.all().order_by('date', 'id')

    # ----- Running balance -----
    running = client.opening_balance
    rows = []
    for entry in entries:
        running += entry.signed_amount
        rows.append({'entry': entry, 'balance': running})

    # ----- Overall totals -----
    total_sales = entries.filter(entry_type='SALE').aggregate(
        t=Sum('amount'))['t'] or Decimal('0.00')

    total_payments = entries.filter(entry_type='PAYMENT').aggregate(
        t=Sum('payment_amount'))['t'] or Decimal('0.00')

    total_quantity = entries.filter(entry_type='SALE').aggregate(
        t=Sum('quantity'))['t'] or Decimal('0.00')

    grand_total = client.opening_balance + total_sales
    remaining_balance = grand_total - total_payments

    # ----- Current month breakdown -----
    today = date.today()
    month_first = today.replace(day=1)
    month_last = date(today.year, today.month, monthrange(today.year, today.month)[1])

    # Current month sales
    current_month_sales = entries.filter(
        entry_type='SALE', date__range=(month_first, month_last)
    ).aggregate(t=Sum('amount'))['t'] or Decimal('0.00')

    # Current month payments
    current_month_payments = entries.filter(
        entry_type='PAYMENT', payment_date__range=(month_first, month_last)
    ).aggregate(t=Sum('payment_amount'))['t'] or Decimal('0.00')

    # Previous month closing balance
    prev_month_end = month_first - timedelta(days=1)
    prev_month_sales = entries.filter(
        entry_type='SALE', date__lte=prev_month_end
    ).aggregate(t=Sum('amount'))['t'] or Decimal('0.00')
    prev_month_payments = entries.filter(
        entry_type='PAYMENT', payment_date__lte=prev_month_end
    ).aggregate(t=Sum('payment_amount'))['t'] or Decimal('0.00')

    previous_month_balance = (
        client.opening_balance + prev_month_sales - prev_month_payments
    )

    # ----- Chart: monthly sales & payments (last 6 months) -----
    labels = []
    sales_series = []
    payment_series = []

    for offset in range(5, -1, -1):
        first, last = _month_bounds(today, offset)
        labels.append(first.strftime('%b %Y'))

        m_sales = entries.filter(
            entry_type='SALE', date__range=(first, last)
        ).aggregate(t=Sum('amount'))['t'] or 0

        m_pay = entries.filter(
            entry_type='PAYMENT', payment_date__range=(first, last)
        ).aggregate(t=Sum('payment_amount'))['t'] or 0

        sales_series.append(float(m_sales))
        payment_series.append(float(m_pay))

    # ----- Payments list (right panel like Excel) -----
    payments_list = entries.filter(
        entry_type='PAYMENT'
    ).order_by('payment_date')

    context = {
        'client': client,
        'rows': rows,
        'total_sales': total_sales,
        'total_payments': total_payments,
        'total_quantity': total_quantity,
        'grand_total': grand_total,
        'remaining_balance': remaining_balance,

        # New summary block for the "Excel-style" totals
        'current_month_amount': current_month_sales,
        'previous_month_balance': previous_month_balance,
        'current_month_payments': current_month_payments,

        'payments_list': payments_list,

        'chart_labels_json': json.dumps(labels),
        'chart_sales_json': json.dumps(sales_series),
        'chart_payments_json': json.dumps(payment_series),
    }
    return render(request, 'ledger/client_ledger.html', context)


# =====================================================================
# ADD CLIENT
# =====================================================================

@login_required
@staff_only
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f"Client '{client.name}' added.")
            return redirect('ledger:client_ledger', client_id=client.id)
    else:
        form = ClientForm()
    return render(request, 'ledger/add_client.html', {'form': form})


# =====================================================================
# ADD ENTRY
# =====================================================================

@login_required
@staff_only
def add_entry(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        form = LedgerEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.client = client
            entry.save()
            messages.success(request, f"Entry added for {client.name}.")
            return redirect('ledger:client_ledger', client_id=client.id)
    else:
        form = LedgerEntryForm(initial={'date': date.today()})

    return render(request, 'ledger/add_entry.html', {
        'form': form,
        'client': client,
    })


# =====================================================================
# EDIT ENTRY
# =====================================================================

@login_required
@staff_only
def edit_entry(request, entry_id):
    entry = get_object_or_404(LedgerEntry, id=entry_id)
    client = entry.client

    if request.method == 'POST':
        form = LedgerEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Entry updated successfully.")
            return redirect('ledger:client_ledger', client_id=client.id)
    else:
        form = LedgerEntryForm(instance=entry)

    return render(request, 'ledger/add_entry.html', {
        'form': form,
        'client': client,
        'is_edit': True,
        'entry': entry,
    })


# =====================================================================
# DELETE ENTRY
# =====================================================================

@login_required
@staff_only
def delete_entry(request, entry_id):
    entry = get_object_or_404(LedgerEntry, id=entry_id)
    client = entry.client

    if request.method == 'POST':
        entry.delete()
        messages.success(request, "Entry deleted.")
        return redirect('ledger:client_ledger', client_id=client.id)

    # GET shows a confirmation page
    return render(request, 'ledger/confirm_delete.html', {
        'entry': entry,
        'client': client,
    })