from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from datetime import date
from calendar import monthrange

from .models import Inventory
from .forms import InventoryForm


staff_only = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='/login/',
)


def _month_range(reference, offset):
    """Return (first_day, last_day) of month offset months before reference."""
    year = reference.year
    month = reference.month - offset
    while month <= 0:
        month += 12
        year -= 1
    first = date(year, month, 1)
    last = date(year, month, monthrange(year, month)[1])
    return first, last


@login_required
@staff_only
def inventory_view(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:inventory')
    else:
        form = InventoryForm()

    data = Inventory.objects.all().order_by('-date', '-id')

    # ---------- Material-wise stock totals ----------
    stock = {'HDPE': 0, 'LDPE': 0, 'PP': 0}
    totals = Inventory.objects.values('material').annotate(total=Sum('quantity'))
    for row in totals:
        if row['material'] in stock and row['total']:
            stock[row['material']] = row['total']

    # ---------- Chart 1: Stock distribution (doughnut) ----------
    stock_chart_labels = ['HDPE', 'LDPE', 'PP']
    stock_chart_data = [
        float(stock.get('HDPE', 0)),
        float(stock.get('LDPE', 0)),
        float(stock.get('PP', 0)),
    ]

    # ---------- Chart 2: Monthly additions (last 6 months, bar) ----------
    today = date.today()
    monthly_labels = []
    monthly_data = []

    for offset in range(5, -1, -1):
        first, last = _month_range(today, offset)
        monthly_labels.append(first.strftime('%b %Y'))

        month_total = Inventory.objects.filter(
            date__range=(first, last)
        ).aggregate(t=Sum('quantity'))['t'] or 0

        monthly_data.append(float(month_total))

    context = {
        'form': form,
        'data': data,
        'stock': stock,

        # Chart data
        'stock_chart_labels': stock_chart_labels,
        'stock_chart_data': stock_chart_data,
        'monthly_labels': monthly_labels,
        'monthly_data': monthly_data,
    }
    return render(request, 'inventory/inventory.html', context)