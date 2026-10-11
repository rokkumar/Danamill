/* ============================================================
   Ledger — Single client view
   Monthly sales vs payments line chart
   ============================================================ */

(function () {
    'use strict';

    function readJSON(id) {
        var el = document.getElementById(id);
        return el ? JSON.parse(el.textContent) : [];
    }

    document.addEventListener('DOMContentLoaded', function () {
        var canvas = document.getElementById('ledgerChart');
        if (!canvas || typeof Chart === 'undefined') return;

        var isLight = document.body.classList.contains('light-mode');
        var textColor = isLight ? '#0f172a' : '#94a3b8';
        var gridColor = isLight ? 'rgba(15,23,42,0.08)' : 'rgba(255,255,255,0.08)';

        new Chart(canvas.getContext('2d'), {
            type: 'line',
            data: {
                labels: readJSON('chart-labels'),
                datasets: [
                    {
                        label: 'Sales (₹)',
                        data: readJSON('chart-sales'),
                        borderColor: '#4f46e5',
                        backgroundColor: 'rgba(79,70,229,0.12)',
                        tension: 0.35,
                        fill: true,
                        borderWidth: 2,
                        pointRadius: 4,
                        pointBackgroundColor: '#4f46e5',
                    },
                    {
                        label: 'Payments (₹)',
                        data: readJSON('chart-payments'),
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16,185,129,0.12)',
                        tension: 0.35,
                        fill: true,
                        borderWidth: 2,
                        pointRadius: 4,
                        pointBackgroundColor: '#10b981',
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: textColor, padding: 14 },
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: textColor },
                        grid: { color: gridColor },
                    },
                    x: {
                        ticks: { color: textColor },
                        grid: { color: gridColor },
                    },
                },
            },
        });
    });
})();