from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum

from .models import Finance
from .forms import IncomeForm, ExpenseForm


staff_only = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='/login/',
)


# =====================================================================
# INCOME
# =====================================================================

@login_required
@staff_only
def income_view(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.transaction_type = 'Income'
            record.save()
            return redirect('finance:income')
    else:
        form = IncomeForm()

    income_qs = Finance.objects.filter(
        transaction_type='Income'
    ).order_by('-date', '-id')

    total_income = income_qs.filter(
        status='Completed'
    ).aggregate(t=Sum('amount'))['t'] or 0

    context = {
        'form': form,
        'income_data': income_qs,
        'total_income': total_income,
    }
    return render(request, 'finance/income.html', context)


# =====================================================================
# EXPENSE
# =====================================================================

@login_required
@staff_only
def expense_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.transaction_type = 'Expense'
            record.save()
            return redirect('finance:expense')
    else:
        form = ExpenseForm()

    expense_qs = Finance.objects.filter(
        transaction_type='Expense'
    ).order_by('-date', '-id')

    total_expense = expense_qs.filter(
        status='Completed'
    ).aggregate(t=Sum('amount'))['t'] or 0

    context = {
        'form': form,
        'expense_data': expense_qs,
        'total_expense': total_expense,
    }
    return render(request, 'finance/expense.html', context)