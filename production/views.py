from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Avg, Count

from .models import Production
from .forms import ProductionForm


staff_only = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='/login/',
)


# =====================================================================
# PRODUCTION ENTRY PAGE
# =====================================================================

@login_required
@staff_only
def production_view(request):
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('production:production')
    else:
        form = ProductionForm()

    qs = Production.objects.all()

    # ---------- Aggregates ----------
    agg = qs.aggregate(
        total_output=Sum('output'),
        total_scrap=Sum('scrap'),
        avg_efficiency=Avg('efficiency'),
    )

    total_entries = qs.count()
    total_output = agg['total_output'] or 0
    total_scrap = agg['total_scrap'] or 0
    avg_efficiency = round(agg['avg_efficiency'] or 0, 1)
    avg_output = round(total_output / total_entries, 1) if total_entries else 0

    recent_production = qs[:10]

    # ---------- Chart: Output per machine ----------
    machine_qs = qs.values('machine').annotate(total=Sum('output'))
    machine_map = {row['machine']: float(row['total'] or 0) for row in machine_qs}

    machine_labels = ['Machine 1', 'Machine 2', 'Machine 3']
    machine_data = [
        machine_map.get('Machine 1', 0),
        machine_map.get('Machine 2', 0),
        machine_map.get('Machine 3', 0),
    ]

    # ---------- Chart: Shift distribution ----------
    shift_qs = qs.values('shift').annotate(c=Count('id'))
    shift_map = {row['shift']: row['c'] for row in shift_qs}

    shift_labels = ['Morning', 'Evening', 'Night']
    shift_data = [
        shift_map.get('Morning', 0),
        shift_map.get('Evening', 0),
        shift_map.get('Night', 0),
    ]

    context = {
        'form': form,
        'recent_production': recent_production,
        'total_entries': total_entries,
        'total_output': total_output,
        'total_scrap': total_scrap,
        'avg_output': avg_output,
        'avg_efficiency': avg_efficiency,

        # Chart data — plain Python lists (JSON conversion happens in template)
        'machine_labels': machine_labels,
        'machine_data': machine_data,
        'shift_labels': shift_labels,
        'shift_data': shift_data,
    }
    return render(request, 'production/production.html', context)


# =====================================================================
# BATCHES LIST PAGE
# =====================================================================

@login_required
@staff_only
def batches_view(request):
    batches = Production.objects.all()
    return render(request, 'production/batches.html', {'batches': batches})


# =====================================================================
# ANALYTICS PAGE
# =====================================================================

@login_required
@staff_only
def analytics_view(request):
    qs = Production.objects.all().order_by('-production_date', '-id')

    recent = list(qs[:7])

    # ---------- Chart: Output per batch ----------
    output_labels = [str(p.batch) for p in recent]
    output_data = [float(p.output) for p in recent]

    # ---------- Chart: Scrap per machine ----------
    scrap_labels = [str(p.machine) for p in recent]
    scrap_data = [float(p.scrap) for p in recent]

    # ---------- Chart: Efficiency per batch ----------
    efficiency_labels = [str(p.batch) for p in recent]
    efficiency_data = [float(p.efficiency) for p in recent]

    # ---------- Chart: Shift distribution ----------
    shift_qs = qs.values('shift').annotate(c=Count('id'))
    shift_map = {row['shift']: row['c'] for row in shift_qs}

    shift_labels = ['Morning', 'Evening', 'Night']
    shift_data = [
        shift_map.get('Morning', 0),
        shift_map.get('Evening', 0),
        shift_map.get('Night', 0),
    ]

    context = {
        'output_labels': output_labels,
        'output_data': output_data,
        'scrap_labels': scrap_labels,
        'scrap_data': scrap_data,
        'efficiency_labels': efficiency_labels,
        'efficiency_data': efficiency_data,
        'shift_labels': shift_labels,
        'shift_data': shift_data,
    }
    return render(request, 'production/analytics.html', context)