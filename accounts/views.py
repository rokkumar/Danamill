from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.db.models import Sum
from django.views.decorators.http import require_POST


staff_only = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='/login/',
)


@login_required
@staff_only
def dashboard(request):
    """
    Main ERP dashboard — shows summary from all modules.
    Only staff users can access.
    """
    from inventory.models import Inventory
    from workforce.models import Employee
    from finance.models import Finance
    from ledger.models import Client

    total_inventory = Inventory.objects.aggregate(t=Sum('quantity'))['t'] or 0
    total_employees = Employee.objects.count()
    total_clients = Client.objects.count()

    income = Finance.objects.filter(
        transaction_type='Income', status='Completed'
    ).aggregate(t=Sum('amount'))['t'] or 0

    expense = Finance.objects.filter(
        transaction_type='Expense', status='Completed'
    ).aggregate(t=Sum('amount'))['t'] or 0

    context = {
        'total_inventory': total_inventory,
        'total_employees': total_employees,
        'total_clients': total_clients,
        'total_income': income,
        'total_expense': expense,
        'profit': income - expense,
    }
    return render(request, 'dashboard/index.html', context)


@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')