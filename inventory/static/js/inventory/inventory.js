/* ============================================================
   Inventory module — charts + form feedback
   ============================================================ */

(function () {
    'use strict';

    function readJSON(id) {
        var el = document.getElementById(id);
        if (!el) return [];
        try {
            return JSON.parse(el.textContent);
        } catch (e) {
            console.error('[Inventory] JSON parse failed for', id, e);
            return [];
        }
    }

    function hasData(arr) {
        return Array.isArray(arr) && arr.length > 0 && arr.some(function (v) {
            return Number(v) > 0;
        });
    }

    function themeColors() {
        var light = document.body.classList.contains('light-mode');
        return {
            text:   light ? '#0f172a' : '#94a3b8',
            grid:   light ? 'rgba(15,23,42,0.08)' : 'rgba(255,255,255,0.08)',
            border: light ? '#ffffff' : '#020617',
        };
    }

    function showEmpty(canvas, message) {
        var parent = canvas.parentNode;
        if (parent) {
            parent.innerHTML = '<div class="chart-empty">' + message + '</div>';
        }
    }

    document.addEventListener('DOMContentLoaded', function () {

        // ============================================================
        // Form feedback
        // ============================================================
        var form = document.querySelector('.inventory-form');
        if (form) {
            form.addEventListener('submit', function () {
                var btn = form.querySelector('.submit-btn');
                if (btn) {
                    btn.disabled = true;
                    btn.textContent = 'Adding...';
                }
            });
        }

        // ============================================================
        // Charts
        // ============================================================
        if (typeof Chart === 'undefined') return;

        var colors = themeColors();

        // ---------- Stock distribution doughnut ----------
        var stockCanvas = document.getElementById('stockChart');
        if (stockCanvas) {
            var stockData = readJSON('stock-data');
            if (!hasData(stockData)) {
                showEmpty(stockCanvas, 'No stock data yet');
            } else {
                new Chart(stockCanvas, {
                    type: 'doughnut',
                    data: {
                        labels: readJSON('stock-labels'),
                        datasets: [{
                            data: stockData,
                            backgroundColor: ['#312e81', '#10b981', '#ef4444'],
                            borderColor: colors.border,
                            borderWidth: 3,
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        animation: { duration: 700 },
                        cutout: '62%',
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: { color: colors.text, padding: 16 }
                            },
                            tooltip: {
                                backgroundColor: '#0f172a',
                                titleColor: '#ffffff',
                                bodyColor: '#cbd5e1',
                                borderColor: '#334155',
                                borderWidth: 1,
                                padding: 10,
                                cornerRadius: 8,
                            }
                        }
                    }
                });
            }
        }

        // ---------- Monthly additions bar ----------
        var monthlyCanvas = document.getElementById('monthlyChart');
        if (monthlyCanvas) {
            var monthlyData = readJSON('monthly-data');
            if (!hasData(monthlyData)) {
                showEmpty(monthlyCanvas, 'No monthly data yet');
            } else {
                new Chart(monthlyCanvas, {
                    type: 'bar',
                    data: {
                        labels: readJSON('monthly-labels'),
                        datasets: [{
                            label: 'Added (Kg)',
                            data: monthlyData,
                            backgroundColor: '#6366f1',
                            borderRadius: 10,
                            borderSkipped: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        animation: { duration: 700 },
                        plugins: {
                            legend: { labels: { color: colors.text } },
                            tooltip: {
                                backgroundColor: '#0f172a',
                                titleColor: '#ffffff',
                                bodyColor: '#cbd5e1',
                                borderColor: '#334155',
                                borderWidth: 1,
                                padding: 10,
                                cornerRadius: 8,
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: { color: colors.text },
                                grid: { color: colors.grid },
                            },
                            x: {
                                ticks: { color: colors.text },
                                grid: { display: false },
                            }
                        }
                    }
                });
            }
        }
    });
})();