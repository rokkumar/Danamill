/* ============================================================
   ERP Base — Sidebar, Submenus, Theme
   Complete working version with localStorage persistence
   ============================================================ */

(function () {
    'use strict';

    var MOBILE_BREAKPOINT = 768;

    function isMobile() {
        return window.innerWidth <= MOBILE_BREAKPOINT;
    }

    // ============================================================
    // SIDEBAR TOGGLE
    // Desktop: collapse/expand
    // Mobile: off-canvas slide
    // ============================================================
    window.toggleSidebar = function () {
        var sidebar = document.getElementById('sidebar');
        var main = document.getElementById('main');
        var overlay = document.getElementById('sidebarOverlay');

        if (!sidebar) return;

        if (isMobile()) {
            // ---------- Mobile ----------
            var isOpen = document.body.classList.contains('sidebar-open');
            if (isOpen) {
                document.body.classList.remove('sidebar-open');
                if (overlay) overlay.classList.remove('active');
                document.body.style.overflow = '';
            } else {
                document.body.classList.add('sidebar-open');
                if (overlay) overlay.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        } else {
            // ---------- Desktop ----------
            var isCollapsed = sidebar.classList.toggle('collapsed');
            if (main) main.classList.toggle('collapsed', isCollapsed);

            // Save preference
            try {
                localStorage.setItem('sidebarCollapsed', isCollapsed ? 'true' : 'false');
            } catch (e) {}
        }
    };

    window.closeSidebar = function () {
        document.body.classList.remove('sidebar-open');
        var overlay = document.getElementById('sidebarOverlay');
        if (overlay) overlay.classList.remove('active');
        document.body.style.overflow = '';
    };

    // ============================================================
    // SUBMENU TOGGLE
    // ============================================================
    window.toggleMenu = function (menuId) {
        var menu = document.getElementById(menuId);
        if (!menu) return;
        menu.classList.toggle('show');
    };

    // ============================================================
    // THEME TOGGLE — SVG icons
    // ============================================================
    var sunSVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';

    var moonSVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

    window.toggleTheme = function () {
        var isLight = document.body.classList.toggle('light-mode');
        try {
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
        } catch (e) {}
        updateThemeIcon(isLight);
    };

    function updateThemeIcon(isLight) {
        var btn = document.getElementById('themeBtn');
        if (btn) btn.innerHTML = isLight ? sunSVG : moonSVG;
    }

    // ============================================================
    // INIT
    // ============================================================
    document.addEventListener('DOMContentLoaded', function () {

        // ---------- Auto-open submenu for current section ----------
        var path = window.location.pathname;

        if (path.indexOf('/dashboard/production/') === 0) {
            var m = document.getElementById('productionSubmenu');
            if (m) m.classList.add('show');
        }
        if (path.indexOf('/dashboard/finance/') === 0) {
            var f = document.getElementById('financeSubmenu');
            if (f) f.classList.add('show');
        }

        // ---------- Restore sidebar collapsed state (desktop only) ----------
        if (!isMobile()) {
            try {
                var saved = localStorage.getItem('sidebarCollapsed');
                if (saved === 'true') {
                    var sidebar = document.getElementById('sidebar');
                    var main = document.getElementById('main');
                    if (sidebar) sidebar.classList.add('collapsed');
                    if (main) main.classList.add('collapsed');
                }
            } catch (e) {}
        }

        // ---------- Mobile: close sidebar on nav link click ----------
        if (isMobile()) {
            document.querySelectorAll('.sidebar-nav a').forEach(function (a) {
                a.addEventListener('click', function () {
                    window.closeSidebar();
                });
            });
        }

        // ---------- Theme init ----------
        var savedTheme = null;
        try {
            savedTheme = localStorage.getItem('theme');
        } catch (e) {}

        if (savedTheme === 'light') {
            document.body.classList.add('light-mode');
            updateThemeIcon(true);
        } else {
            updateThemeIcon(false);
        }
    });

    // ============================================================
    // RESIZE HANDLER
    // ============================================================
    var resizeTimer;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
            if (!isMobile()) {
                // Returning to desktop — close any mobile-open state
                document.body.classList.remove('sidebar-open');
                document.body.style.overflow = '';
                var overlay = document.getElementById('sidebarOverlay');
                if (overlay) overlay.classList.remove('active');
            }
        }, 120);
    });

})();