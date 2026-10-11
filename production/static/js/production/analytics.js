/* ============================================================
   Production — Analytics page charts
   ============================================================ */

(function () {
    'use strict';

    function readJSON(id) {
        var el = document.getElementById(id);
        if (!el) {
            console.warn('[Analytics] Missing JSON element:', id);
            return [];
        }
        try {
            return JSON.parse(el.textContent);
        } catch (e) {
            console.error('[Analytics] Failed to parse', id, e);
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

    // Common options
    function chartOptions(colors, extra) {
        var base = {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 700 },
            plugins: {
                legend: {
                    labels: { color: colors.text, font: { size: 12 } },
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
        };
        if (extra) {
            Object.assign(base, extra);
        }
        return base;
    }

    document.addEventListener('DOMContentLoaded', function () {
        if (typeof Chart === 'undefined') {
            console.error('[Analytics] Chart.js not loaded');
            return;
        }

        var colors = themeColors();

        // ============================================================
        // 1. Output Line Chart
        // ============================================================
        var outputCanvas = document.getElementById('outputChart');
        if (outputCanvas) {
            var outputData = readJSON('output-data');
            if (!hasData(outputData)) {
                showEmpty(outputCanvas, 'No output data yet');
            } else {
                new Chart(outputCanvas, {
                    type: 'line',
                    data: {
                        labels: readJSON('output-labels'),
                        datasets: [{
                            label: 'Output (kg)',
                            data: outputData,
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16,185,129,0.15)',
                            fill: true,
                            tension: 0.35,
                            borderWidth: 2,
                            pointRadius: 4,
                            pointBackgroundColor: '#10b981',
                        }]
                    },
                    options: chartOptions(colors, {
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: { color: colors.text },
                                grid: { color: colors.grid },
                            },
                            x: {
                                ticks: { color: colors.text },
                                grid: { color: colors.grid },
                            },
                        },
                    }),
                });
            }
        }

        // ============================================================
        // 2. Scrap Bar Chart
        // ============================================================
        var scrapCanvas = document.getElementById('scrapChart');
        if (scrapCanvas) {
            var scrapData = readJSON('scrap-data');
            if (!hasData(scrapData)) {
                showEmpty(scrapCanvas, 'No scrap data yet');
            } else {
                new Chart(scrapCanvas, {
                    type: 'bar',
                    data: {
                        labels: readJSON('scrap-labels'),
                        datasets: [{
                            label: 'Scrap (kg)',
                            data: scrapData,
                            backgroundColor: ['#ef4444', '#f97316', '#eab308', '#8b5cf6', '#10b981', '#6366f1', '#f59e0b'],
                            borderRadius: 10,
                            borderSkipped: false,
                        }]
                    },
                    options: chartOptions(colors, {
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
                    }),
                });
            }
        }

        // ============================================================
        // 3. Efficiency Doughnut
        // ============================================================
        var efficiencyCanvas = document.getElementById('efficiencyChart');
        if (efficiencyCanvas) {
            var efficiencyData = readJSON('efficiency-data');
            if (!hasData(efficiencyData)) {
                showEmpty(efficiencyCanvas, 'No efficiency data yet');
            } else {
                new Chart(efficiencyCanvas, {
                    type: 'doughnut',
                    data: {
                        labels: readJSON('efficiency-labels'),
                        datasets: [{
                            data: efficiencyData,
                            backgroundColor: ['#8b5cf6', '#6366f1', '#10b981', '#f59e0b', '#ef4444', '#14b8a6', '#eab308'],
                            borderColor: colors.border,
                            borderWidth: 3,
                            hoverOffset: 10,
                        }]
                    },
                    options: chartOptions(colors, {
                        cutout: '62%',
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: { color: colors.text, padding: 14, font: { size: 12 } },
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
                    }),
                });
            }
        }

        // ============================================================
        // 4. Shift Polar Chart
        // ============================================================
        var shiftCanvas = document.getElementById('shiftAnalyticsChart');
        if (shiftCanvas) {
            var shiftData = readJSON('shift-data');
            if (!hasData(shiftData)) {
                showEmpty(shiftCanvas, 'No shift data yet');
            } else {
                new Chart(shiftCanvas, {
                    type: 'polarArea',
                    data: {
                        labels: readJSON('shift-labels'),
                        datasets: [{
                            data: shiftData,
                            backgroundColor: ['#f59e0b', '#10b981', '#6366f1'],
                            borderColor: colors.border,
                            borderWidth: 2,
                        }]
                    },
                    options: chartOptions(colors, {
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: { color: colors.text, padding: 14, font: { size: 12 } },
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
                        scales: {
                            r: {
                                ticks: { color: colors.text },
                                grid: { color: colors.grid },
                            },
                        },
                    }),
                });
            }
        }
    });
})();