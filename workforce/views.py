from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.db.models import Sum, Avg

from .models import Employee
from .forms import EmployeeForm


staff_only = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='/login/',
)


@login_required
@staff_only
def workforce_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workforce:workforce')
    else:
        form = EmployeeForm()

    employees = Employee.objects.all().order_by('-id')

    total = employees.count()
    present = employees.filter(attendance=True).count()
    absent = total - present

    avg = employees.aggregate(a=Avg('productivity'))['a']
    avg_productivity = round(avg) if avg else 0

    context = {
        'form': form,
        'employees': employees,
        'total': total,
        'present': present,
        'absent': absent,
        'avg_productivity': avg_productivity,
    }
    return render(request, 'workforce/workforce.html', context)


@login_required
@staff_only
@require_POST
def delete_employee(request, id):
    emp = get_object_or_404(Employee, id=id)
    emp.delete()
    return redirect('workforce:workforce')


@login_required
@staff_only
@require_POST
def toggle_attendance(request, id):
    emp = get_object_or_404(Employee, id=id)
    emp.attendance = not emp.attendance
    emp.save(update_fields=['attendance'])
    return redirect('workforce:workforce')