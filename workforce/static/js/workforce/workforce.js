/* ============================================================
   Workforce module — progress bars, delete confirmation
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    // Animate progress bars
    document.querySelectorAll('.progress-bar').forEach(function (bar) {
        var width = parseInt(bar.getAttribute('data-width') || '0', 10);
        if (width < 0) width = 0;
        if (width > 100) width = 100;
        // Small delay so the transition runs
        setTimeout(function () {
            bar.style.width = width + '%';
        }, 60);
    });

    // Confirm before deleting an employee
    document.querySelectorAll('.js-delete-form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            if (!confirm('Delete this employee? This cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

});