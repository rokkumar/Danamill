"""
Dashboard view for the ERP system.
Aggregates data from Inventory, Workforce, Finance, Ledger, Production, Dispatch, Quality.
"""

from decimal import Decimal
from datetime import date
from calendar import monthrange

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Avg

from inventory.models import Inventory
from workforce.models import Employee
from finance.models import Finance
from ledger.models import Client
from production.models import Production
from dispatch.models import Dispatch
from quality.models import Quality


staff_only = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='/login/',
)


# ============================================================
# Helpers
# ============================================================

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


def _percent_change(current, previous):
    """Return percentage change between two numbers."""
    try:
        current = float(current)
        previous = float(previous)
    except (TypeError, ValueError):
        return 0
    if previous == 0:
        return 100 if current > 0 else 0
    return round(((current - previous) / previous) * 100, 1)


# ============================================================
# Dashboard
# ============================================================

@login_required
@staff_only
def dashboard_view(request):

    today = date.today()

    # ---------------------------------------------------------
    # 1. INVENTORY
    # ---------------------------------------------------------
    inv_qs = Inventory.objects.all()
    total_inventory = inv_qs.aggregate(t=Sum('quantity'))['t'] or 0
    recent_inventory = inv_qs.order_by('-id')[:5]

    material_totals = {
        row['material']: row['total'] or 0
        for row in inv_qs.values('material').annotate(total=Sum('quantity'))
    }
    inventory_chart_labels = ['HDPE', 'LDPE', 'PP']
    inventory_chart_data = [
        float(material_totals.get('HDPE', 0)),
        float(material_totals.get('LDPE', 0)),
        float(material_totals.get('PP', 0)),
    ]

    # ---------------------------------------------------------
    # 2. WORKFORCE
    # ---------------------------------------------------------
    emp_qs = Employee.objects.all()
    total_workforce = emp_qs.count()
    present_count = emp_qs.filter(attendance=True).count()
    absent_count = total_workforce - present_count

    avg_productivity = emp_qs.aggregate(a=Avg('productivity'))['a']
    avg_productivity = round(avg_productivity, 1) if avg_productivity else 0

    recent_employees = emp_qs.order_by('-id')[:5]

    top_performers = emp_qs.order_by('-productivity')[:7]
    productivity_labels = [e.name[:10] for e in top_performers]
    productivity_data = [e.productivity for e in top_performers]

    shift_counts = {
        row['shift']: row['c']
        for row in emp_qs.values('shift').annotate(c=Count('id'))
    }
    shift_labels = ['Morning', 'Evening', 'Night']
    shift_data = [
        shift_counts.get('Morning', 0),
        shift_counts.get('Evening', 0),
        shift_counts.get('Night', 0),
    ]

    # ---------------------------------------------------------
    # 3. FINANCE
    # ---------------------------------------------------------
    completed = Finance.objects.filter(status='Completed')

    total_income = completed.filter(
        transaction_type='Income'
    ).aggregate(t=Sum('amount'))['t'] or Decimal('0.00')

    total_expense = completed.filter(
        transaction_type='Expense'
    ).aggregate(t=Sum('amount'))['t'] or Decimal('0.00')

    total_profit = total_income - total_expense

    this_month_first, this_month_last = _month_range(today, 0)
    prev_month_first, prev_month_last = _month_range(today, 1)

    this_month_income = completed.filter(
        transaction_type='Income',
        date__range=(this_month_first, this_month_last),
    ).aggregate(t=Sum('amount'))['t'] or 0

    prev_month_income = completed.filter(
        transaction_type='Income',
        date__range=(prev_month_first, prev_month_last),
    ).aggregate(t=Sum('amount'))['t'] or 0

    income_growth = _percent_change(this_month_income, prev_month_income)

    recent_finance = Finance.objects.order_by('-date', '-id')[:6]

    finance_labels = ['Income', 'Expense', 'Profit']
    finance_data = [
        float(total_income),
        float(total_expense),
        float(total_profit),
    ]

    # Expense categories — ✅ FIXED: same variable name everywhere
    category_totals = {
        row['category']: float(row['total'] or 0)
        for row in completed.filter(transaction_type='Expense')
        .values('category')
        .annotate(total=Sum('amount'))
    }
    expense_categories = ['Raw Material', 'Salary', 'Transport', 'Maintenance']
    expense_category_labels = expense_categories          # ✅ Same name
    expense_category_data = [category_totals.get(c, 0) for c in expense_categories]

    # ---------------------------------------------------------
    # 4. LEDGER
    # ---------------------------------------------------------
    total_clients = Client.objects.count()

    total_outstanding = Decimal('0.00')
    for c in Client.objects.all():
        total_outstanding += c.outstanding()

    # ---------------------------------------------------------
    # 5. PRODUCTION
    # ---------------------------------------------------------
    total_output = Production.objects.aggregate(t=Sum('output'))['t'] or 0

    # ---------------------------------------------------------
    # 6. DISPATCH
    # ---------------------------------------------------------
    total_dispatches = Dispatch.objects.count()
    pending_dispatches = Dispatch.objects.filter(dispatch_status='Pending').count()

    # ---------------------------------------------------------
    # 7. QUALITY
    # ---------------------------------------------------------
    total_qc_tests = Quality.objects.count()
    passed_qc = Quality.objects.filter(qc_result='Pass').count()
    qc_pass_rate = round((passed_qc / total_qc_tests) * 100, 1) if total_qc_tests else 0

    # ---------------------------------------------------------
    # Context
    # ---------------------------------------------------------
    context = {
        # INVENTORY
        'total_inventory': total_inventory,
        'recent_inventory': recent_inventory,
        'inventory_chart_labels': inventory_chart_labels,
        'inventory_chart_data': inventory_chart_data,

        # WORKFORCE
        'total_workforce': total_workforce,
        'present_count': present_count,
        'absent_count': absent_count,
        'avg_productivity': avg_productivity,
        'recent_employees': recent_employees,
        'productivity_labels': productivity_labels,
        'productivity_data': productivity_data,
        'shift_labels': shift_labels,
        'shift_data': shift_data,

        # FINANCE
        'total_income': total_income,
        'total_expense': total_expense,
        'total_profit': total_profit,
        'income_growth': income_growth,
        'recent_finance': recent_finance,
        'finance_labels': finance_labels,
        'finance_data': finance_data,
        'expense_category_labels': expense_category_labels,
        'expense_category_data': expense_category_data,

        # LEDGER
        'total_clients': total_clients,
        'total_outstanding': total_outstanding,

        # PRODUCTION
        'total_output': total_output,

        # DISPATCH
        'total_dispatches': total_dispatches,
        'pending_dispatches': pending_dispatches,

        # QUALITY
        'total_qc_tests': total_qc_tests,
        'qc_pass_rate': qc_pass_rate,
    }

    return render(request, 'reports/dashboard.html', context)