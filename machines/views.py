from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Avg

from .models import Machine
from .forms import MachineForm


staff_only = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='/login/',
)


@login_required
@staff_only
def machines_view(request):
    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('machines:machines')
    else:
        form = MachineForm()

    qs = Machine.objects.all().order_by('-id')

    # ---------- Summary ----------
    total_machines = qs.count()

    status_counts = {
        row['status']: row['c']
        for row in qs.values('status').annotate(c=Count('id'))
    }
    running_count = status_counts.get('Running', 0)
    idle_count = status_counts.get('Idle', 0)
    breakdown_count = status_counts.get('Breakdown', 0)

    avg_eff = qs.aggregate(a=Avg('efficiency'))['a']
    avg_efficiency = round(float(avg_eff), 1) if avg_eff else 0

    recent_machines = qs[:10]

    # ---------- Chart 1: Status distribution ----------
    status_labels = ['Running', 'Idle', 'Breakdown']
    status_data = [running_count, idle_count, breakdown_count]

    # ---------- Chart 2: RPM of recent machines ----------
    recent_for_chart = list(qs[:7])
    rpm_labels = [str(m.machine_id) for m in recent_for_chart]
    rpm_data = [int(m.rpm) for m in recent_for_chart]

    context = {
        'form': form,
        'recent_machines': recent_machines,
        'total_machines': total_machines,
        'running_count': running_count,
        'idle_count': idle_count,
        'breakdown_count': breakdown_count,
        'avg_efficiency': avg_efficiency,

        # Chart data — plain Python lists
        'status_labels': status_labels,
        'status_data': status_data,
        'rpm_labels': rpm_labels,
        'rpm_data': rpm_data,
    }
    return render(request, 'machines/machines.html', context)