/* ============================================================
   Dashboard Charts — Professional
   ============================================================ */

(function () {
    'use strict';

    function readJSON(id) {
        var el = document.getElementById(id);
        return el ? JSON.parse(el.textContent) : [];
    }

    function isLightMode() {
        return document.body.classList.contains('light-mode');
    }

    function themeColors() {
        var light = isLightMode();
        return {
            text: light ? '#0f172a' : '#94a3b8',
            grid: light ? 'rgba(15,23,42,0.08)' : 'rgba(255,255,255,0.06)',
            border: light ? '#ffffff' : '#0f172a',
        };
    }

    document.addEventListener('DOMContentLoaded', function () {
        if (typeof Chart === 'undefined') return;

        var colors = themeColors();

        // Common chart options
        var commonOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: colors.text,
                        font: { size: 12, weight: '600' },
                        padding: 12,
                    },
                },
                tooltip: {
                    backgroundColor: '#0f172a',
                    titleColor: '#ffffff',
                    bodyColor: '#cbd5e1',
                    borderColor: '#334155',
                    borderWidth: 1,
                    padding: 10,
                    cornerRadius: 8,
                    titleFont: { size: 13, weight: '700' },
                    bodyFont: { size: 12 },
                },
            },
        };

        // -------- Productivity Bar Chart --------
        var prodCanvas = document.getElementById('productivityChart');
        if (prodCanvas) {
            new Chart(prodCanvas, {
                type: 'bar',
                data: {
                    labels: readJSON('productivity-labels'),
                    datasets: [{
                        label: 'Productivity %',
                        data: readJSON('productivity-data'),
                        backgroundColor: ['#7c3aed', '#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444'],
                        borderRadius: 8,
                        borderSkipped: false,
                    }],
                },
                options: Object.assign({}, commonOptions, {
                    scales: {
                        x: {
                            ticks: { color: colors.text, font: { size: 11 }, maxRotation: 0 },
                            grid: { display: false },
                        },
                        y: {
                            beginAtZero: true,
                            ticks: { color: colors.text, font: { size: 11 } },
                            grid: { color: colors.grid },
                        },
                    },
                }),
            });
        }

        // -------- Shift Doughnut Chart --------
        var shiftCanvas = document.getElementById('shiftChart');
        if (shiftCanvas) {
            new Chart(shiftCanvas, {
                type: 'doughnut',
                data: {
                    labels: readJSON('shift-labels'),
                    datasets: [{
                        data: readJSON('shift-data'),
                        backgroundColor: ['#7c3aed', '#eab308', '#10b981'],
                        borderColor: colors.border,
                        borderWidth: 3,
                    }],
                },
                options: Object.assign({}, commonOptions, {
                    cutout: '68%',
                }),
            });
        }

        // -------- Finance Bar Chart --------
        var finCanvas = document.getElementById('financeChart');
        if (finCanvas) {
            new Chart(finCanvas, {
                type: 'bar',
                data: {
                    labels: readJSON('finance-labels'),
                    datasets: [{
                        label: 'Amount (₹)',
                        data: readJSON('finance-data'),
                        backgroundColor: ['#10b981', '#ef4444', '#6366f1'],
                        borderRadius: 10,
                        borderSkipped: false,
                    }],
                },
                options: Object.assign({}, commonOptions, {
                    scales: {
                        x: {
                            ticks: { color: colors.text, font: { size: 11 } },
                            grid: { display: false },
                        },
                        y: {
                            beginAtZero: true,
                            ticks: { color: colors.text, font: { size: 11 } },
                            grid: { color: colors.grid },
                        },
                    },
                }),
            });
        }

        // -------- Expense Doughnut Chart --------
        var expCanvas = document.getElementById('expenseChart');
        if (expCanvas) {
            new Chart(expCanvas, {
                type: 'doughnut',
                data: {
                    labels: readJSON('expense-category-labels'),
                    datasets: [{
                        data: readJSON('expense-category-data'),
                        backgroundColor: ['#ef4444', '#f97316', '#eab308', '#8b5cf6'],
                        borderColor: colors.border,
                        borderWidth: 3,
                    }],
                },
                options: Object.assign({}, commonOptions, {
                    cutout: '65%',
                }),
            });
        }
    });

})();