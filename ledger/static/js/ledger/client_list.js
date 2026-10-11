/* ============================================================
   Ledger — Client list
   Simple client-side search filter
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
    var input = document.getElementById('clientSearch');
    var body = document.getElementById('clientTableBody');

    if (!input || !body) return;

    var rows = body.querySelectorAll('tr');

    input.addEventListener('input', function () {
        var q = this.value.trim().toLowerCase();

        rows.forEach(function (row) {
            var haystack = (row.dataset.search || '').toLowerCase();
            if (!q || haystack.indexOf(q) !== -1) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});