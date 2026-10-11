/* ============================================================
   Machines module — charts
   ============================================================ */

(function () {
    'use strict';

    function readJSON(id) {
        var el = document.getElementById(id);
        if (!el) return [];
        try {
            return JSON.parse(el.textContent);
        } catch (e) {
            console.error('[Machines] JSON parse failed for', id, e);
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
        if (typeof Chart === 'undefined') return;

        var colors = themeColors();

        // ---------- Status doughnut ----------
        var statusCanvas = document.getElementById('statusChart');
        if (statusCanvas) {
            var statusData = readJSON('status-data');
            if (!hasData(statusData)) {
                showEmpty(statusCanvas, 'No machine status data yet');
            } else {
                new Chart(statusCanvas, {
                    type: 'doughnut',
                    data: {
                        labels: readJSON('status-labels'),
                        datasets: [{
                            data: statusData,
                            backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
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

        // ---------- RPM bar ----------
        var rpmCanvas = document.getElementById('rpmChart');
        if (rpmCanvas) {
            var rpmData = readJSON('rpm-data');
            if (!hasData(rpmData)) {
                showEmpty(rpmCanvas, 'No RPM data yet');
            } else {
                new Chart(rpmCanvas, {
                    type: 'bar',
                    data: {
                        labels: readJSON('rpm-labels'),
                        datasets: [{
                            label: 'RPM',
                            data: rpmData,
                            backgroundColor: ['#6366f1', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#14b8a6', '#3b82f6'],
                            borderRadius: 8,
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
                                grid: { color: colors.grid }
                            },
                            x: {
                                ticks: { color: colors.text },
                                grid: { display: false }
                            }
                        }
                    }
                });
            }
        }
    });
})();