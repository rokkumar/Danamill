from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count

from .models import Quality
from .forms import QualityForm


staff_only = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='/login/',
)


@login_required
@staff_only
def quality_view(request):
    if request.method == 'POST':
        form = QualityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quality:quality-app')
    else:
        form = QualityForm()

    qs = Quality.objects.all().order_by('-test_date', '-id')

    # ---------- Summary ----------
    total_tests = qs.count()

    result_counts = {
        row['qc_result']: row['c']
        for row in qs.values('qc_result').annotate(c=Count('id'))
    }
    pass_count = result_counts.get('Pass', 0)
    fail_count = result_counts.get('Fail', 0)

    pass_percentage = round((pass_count / total_tests) * 100, 1) if total_tests else 0

    recent_records = qs[:10]

    # ---------- Chart: QC result distribution ----------
    qc_labels = ['Pass', 'Fail']
    qc_data = [pass_count, fail_count]

    # ---------- Chart: MFI of recent batches ----------
    mfi_records = list(qs[:7])
    mfi_labels = [str(r.batch_id) for r in mfi_records]
    mfi_data = [float(r.mfi) for r in mfi_records]

    context = {
        'form': form,
        'recent_records': recent_records,
        'total_tests': total_tests,
        'pass_count': pass_count,
        'fail_count': fail_count,
        'pass_percentage': pass_percentage,
        'qc_labels': qc_labels,
        'qc_data': qc_data,
        'mfi_labels': mfi_labels,
        'mfi_data': mfi_data,
    }
    return render(request, 'quality/quality.html', context)