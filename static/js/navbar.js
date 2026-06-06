// static/js/navbar.js
// Additional interactions for the navbar (if needed beyond header.js)
// Currently, all interactive features (active link highlighting, dropdowns)
// are handled in header.js. This file can be used for future enhancements.

document.addEventListener('DOMContentLoaded', function() {
    const currentUrl = window.location.pathname;
    document.querySelectorAll('.nav-link, .mobile-nav a, .dropdown-menu a').forEach(link => {
        const href = link.getAttribute('href');
        link.classList.remove('active');
        if (!href || href === '#') return;

        const linkPath = new URL(href, window.location.origin).pathname;
        if (currentUrl === linkPath || (linkPath !== '/' && currentUrl.startsWith(linkPath))) {
            link.classList.add('active');
        }
    });
});
