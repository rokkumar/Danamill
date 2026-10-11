from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count

from .models import Dispatch
from .forms import DispatchForm


staff_only = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='/login/',
)


@login_required
@staff_only
def dispatch_view(request):
    if request.method == 'POST':
        form = DispatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispatch:dispatch')
    else:
        form = DispatchForm()

    qs = Dispatch.objects.all().order_by('-dispatch_date', '-id')

    # ---------- Summary ----------
    total_dispatch = qs.count()

    status_counts = {
        row['dispatch_status']: row['c']
        for row in qs.values('dispatch_status').annotate(c=Count('id'))
    }
    pending_count = status_counts.get('Pending', 0)
    transit_count = status_counts.get('In Transit', 0)
    delivered_count = status_counts.get('Delivered', 0)

    recent_dispatch = qs[:10]

    # ---------- Chart 1: Status distribution ----------
    status_labels = ['Pending', 'In Transit', 'Delivered']
    status_data = [pending_count, transit_count, delivered_count]

    # ---------- Chart 2: Recent quantities ----------
    quantity_qs = list(qs[:7])
    quantity_labels = [str(d.dispatch_id) for d in quantity_qs]
    quantity_data = [int(d.quantity) for d in quantity_qs]

    context = {
        'form': form,
        'recent_dispatch': recent_dispatch,
        'total_dispatch': total_dispatch,
        'pending_count': pending_count,
        'transit_count': transit_count,
        'delivered_count': delivered_count,

        # Chart data — plain Python lists
        'status_labels': status_labels,
        'status_data': status_data,
        'quantity_labels': quantity_labels,
        'quantity_data': quantity_data,
    }
    return render(request, 'dispatch/dispatch.html', context)