

// ========== SET MOBILE MENU POSITION BELOW HEADER ==========
function positionMobileMenu() {
    const header = document.querySelector('.main-header');
    const mobileNav = document.getElementById('mobileNav');
    const mobileOverlay = document.getElementById('mobileOverlay');
    if (header && mobileNav) {
        const headerBottom = Math.max(0, Math.round(header.getBoundingClientRect().bottom));
        mobileNav.style.top = headerBottom + 'px';
        mobileNav.style.maxHeight = `calc(100vh - ${headerBottom}px)`;
        if (mobileOverlay) {
            mobileOverlay.style.top = headerBottom + 'px';
            mobileOverlay.style.height = `calc(100vh - ${headerBottom}px)`;
        }
    }
}

// Run on load, resize, and when dark mode toggles (affects header height)
window.addEventListener('load', positionMobileMenu);
window.addEventListener('resize', positionMobileMenu);
window.addEventListener('scroll', positionMobileMenu, { passive: true });

// Also after any dynamic content changes (like cart update)
const headerElement = document.querySelector('.main-header');
if (headerElement && 'ResizeObserver' in window) {
    const observer = new ResizeObserver(() => positionMobileMenu());
    observer.observe(headerElement);
}

// Re-run when dark mode toggles (if you have dark mode toggle)
const darkToggle = document.getElementById('darkModeToggle');
if (darkToggle) {
    darkToggle.addEventListener('click', () => {
        setTimeout(positionMobileMenu, 30);
    });
}



document.addEventListener('DOMContentLoaded', function() {
    // ========== MOBILE MENU (FIXED) ==========
    const mobileToggle = document.getElementById('mobileMenuToggle');
    const mobileNav = document.getElementById('mobileNav');
    const mobileOverlay = document.getElementById('mobileOverlay');

    function closeMobileMenu() {
        if (mobileNav) mobileNav.classList.remove('active');
        if (mobileOverlay) mobileOverlay.classList.remove('active');
        if (mobileToggle) mobileToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
    }

    if (mobileToggle && mobileNav) {
        mobileToggle.setAttribute('aria-expanded', 'false');
        mobileToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            positionMobileMenu();
            mobileNav.classList.toggle('active');
            if (mobileOverlay) mobileOverlay.classList.toggle('active');
            const isOpen = mobileNav.classList.contains('active');
            mobileToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            document.body.style.overflow = isOpen ? 'hidden' : '';
        });
    }
    if (mobileOverlay) {
        mobileOverlay.addEventListener('click', closeMobileMenu);
    }
    window.addEventListener('resize', () => {
        positionMobileMenu();
        if (window.innerWidth > 992) closeMobileMenu();
    });

    // ========== DARK MODE ==========
    const darkToggle = document.getElementById('darkModeToggle');
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        if (darkToggle) darkToggle.classList.replace('fa-moon', 'fa-sun');
    }
    if (darkToggle) {
        darkToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            darkToggle.classList.toggle('fa-moon', !isDark);
            darkToggle.classList.toggle('fa-sun', isDark);
        });
    }

    // ========== SEARCH DROPDOWN ==========
    const searchIcon = document.getElementById('searchIcon');
    const searchDropdown = document.getElementById('searchDropdown');
    const searchInput = document.getElementById('searchInput');
    const searchSubmit = document.getElementById('searchSubmit');

    if (searchIcon && searchDropdown) {
        searchIcon.addEventListener('click', (e) => {
            e.stopPropagation();
            searchDropdown.classList.toggle('active');
            const cartDrop = document.getElementById('cartDropdown');
            if (cartDrop) cartDrop.classList.remove('active');
        });
    }
    if (searchSubmit && searchInput) {
        searchSubmit.addEventListener('click', () => {
            const query = searchInput.value.trim();
            if (query) window.location.href = `/search/?q=${encodeURIComponent(query)}`;
        });
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') searchSubmit.click();
        });
    }

    // ========== CART DROPDOWN ==========
    const cartIcon = document.getElementById('cartIcon');
    const cartDropdown = document.getElementById('cartDropdown');
    const cartCountSpan = document.getElementById('cartCount');

    function updateCartDropdown() {
        if (!cartDropdown) return;
        fetch('/cart/api/dropdown/')
            .then(response => response.json())
            .then(data => {
                const itemsDiv = cartDropdown.querySelector('.cart-items');
                if (data.items && data.items.length) {
                    itemsDiv.innerHTML = data.items.map(item => `
                        <div class="cart-item">
                            <span>${escapeHtml(item.name)} x${item.qty}</span>
                            <span>₹${item.total}</span>
                        </div>
                    `).join('');
                } else {
                    itemsDiv.innerHTML = 'No items yet.';
                }
                if (cartCountSpan) cartCountSpan.innerText = data.total_items;
            })
            .catch(err => console.error('Cart dropdown error:', err));
    }

    if (cartIcon && cartDropdown) {
        cartIcon.addEventListener('click', (e) => {
            e.stopPropagation();
            updateCartDropdown();
            cartDropdown.classList.toggle('active');
            if (searchDropdown) searchDropdown.classList.remove('active');
        });
    }

    document.addEventListener('click', (e) => {
        if (searchDropdown && !searchDropdown.contains(e.target) && !searchIcon?.contains(e.target))
            searchDropdown.classList.remove('active');
        if (cartDropdown && !cartDropdown.contains(e.target) && !cartIcon?.contains(e.target))
            cartDropdown.classList.remove('active');
    });

    // ========== LIVE CHAT ==========
    const liveChatBtn = document.getElementById('liveChatBtn');
    if (liveChatBtn) liveChatBtn.addEventListener('click', () => alert('Live chat coming soon!'));

    // Helper
    function escapeHtml(str) {
        if (!str) return '';
        return str.replace(/[&<>]/g, function(m) {
            if (m === '&') return '&amp;';
            if (m === '<') return '&lt;';
            if (m === '>') return '&gt;';
            return m;
        });
    }

    updateCartDropdown();
});
