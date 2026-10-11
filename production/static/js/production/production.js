/* ============================================================
   Production — main page charts
   ============================================================ */

(function () {
    'use strict';

    // ---------- Safe JSON reader ----------
    function readJSON(id) {
        var el = document.getElementById(id);
        if (!el) {
            console.warn('[Production] Missing JSON element:', id);
            return [];
        }
        try {
            return JSON.parse(el.textContent);
        } catch (e) {
            console.error('[Production] Failed to parse', id, e);
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
        if (typeof Chart === 'undefined') {
            console.error('[Production] Chart.js not loaded');
            return;
        }

        var colors = themeColors();

        // ============================================================
        // 1. Machine Chart (Bar)
        // ============================================================
        var machineCanvas = document.getElementById('machineChart');
        if (machineCanvas) {
            var machineLabels = readJSON('machine-labels');
            var machineData = readJSON('machine-data');

            if (!hasData(machineData)) {
                showEmpty(machineCanvas, 'No production data yet');
            } else {
                new Chart(machineCanvas, {
                    type: 'bar',
                    data: {
                        labels: machineLabels,
                        datasets: [{
                            label: 'Output (kg)',
                            data: machineData,
                            backgroundColor: ['#7c3aed', '#6366f1', '#10b981'],
                            borderRadius: 10,
                            borderSkipped: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        animation: { duration: 700 },
                        plugins: {
                            legend: { labels: { color: colors.text, font: { size: 12 } } },
                            tooltip: {
                                backgroundColor: '#0f172a',
                                titleColor: '#ffffff',
                                bodyColor: '#cbd5e1',
                                borderColor: '#334155',
                                borderWidth: 1,
                                padding: 10,
                                cornerRadius: 8,
                            },
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
                            },
                        },
                    }
                });
            }
        }

        // ============================================================
        // 2. Shift Chart (Doughnut)
        // ============================================================
        var shiftCanvas = document.getElementById('shiftChart');
        if (shiftCanvas) {
            var shiftLabels = readJSON('shift-labels');
            var shiftData = readJSON('shift-data');

            if (!hasData(shiftData)) {
                showEmpty(shiftCanvas, 'No shift data yet');
            } else {
                new Chart(shiftCanvas, {
                    type: 'doughnut',
                    data: {
                        labels: shiftLabels,
                        datasets: [{
                            data: shiftData,
                            backgroundColor: ['#f59e0b', '#10b981', '#6366f1'],
                            borderColor: colors.border,
                            borderWidth: 3,
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        animation: { duration: 700 },
                        cutout: '60%',
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: { color: colors.text, padding: 16, font: { size: 12 } },
                            },
                            tooltip: {
                                backgroundColor: '#0f172a',
                                titleColor: '#ffffff',
                                bodyColor: '#cbd5e1',
                                borderColor: '#334155',
                                borderWidth: 1,
                                padding: 10,
                                cornerRadius: 8,
                            },
                        },
                    }
                });
            }
        }
    });
})();