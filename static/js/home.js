// AOS Init
AOS.init({ duration: 1000, once: true });

// Toast Function
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast-notification';

    toast.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i> ${message}`;

    toast.style.cssText = `
        position: fixed;
        bottom: 100px;
        right: 20px;
        background: linear-gradient(135deg, #1a4a8a, #2c6e9e);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        z-index: 9999;
        animation: slideInRight 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    `;

    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Elements
const mobileToggle = document.getElementById('mobileToggle');
const navMenu = document.getElementById('navMenu');
const mobileOverlay = document.getElementById('mobileOverlay');
const searchToggle = document.getElementById('searchToggle');
const searchDropdown = document.getElementById('searchDropdown');
const cartBtn = document.getElementById('cartBtn');
const cartDropdown = document.getElementById('cartDropdown');
const themeToggle = document.getElementById('themeToggle');
const backToTop = document.getElementById('backToTopFooter');

// Mobile Menu
if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        if (mobileOverlay) mobileOverlay.classList.toggle('active');

        document.body.style.overflow =
            navMenu.classList.contains('active') ? 'hidden' : '';
    });
}

if (mobileOverlay) {
    mobileOverlay.addEventListener('click', () => {
        navMenu.classList.remove('active');
        mobileOverlay.classList.remove('active');
        document.body.style.overflow = '';
    });
}

// Search Toggle
if (searchToggle && searchDropdown) {
    searchToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        searchDropdown.classList.toggle('active');
        if (cartDropdown) cartDropdown.classList.remove('active');
    });
}

// Cart Toggle
if (cartBtn && cartDropdown) {
    cartBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        cartDropdown.classList.toggle('active');
        if (searchDropdown) searchDropdown.classList.remove('active');
    });
}

// Close dropdown outside click
document.addEventListener('click', (e) => {
    if (searchDropdown && !searchDropdown.contains(e.target) && !searchToggle?.contains(e.target)) {
        searchDropdown.classList.remove('active');
    }

    if (cartDropdown && !cartDropdown.contains(e.target) && !cartBtn?.contains(e.target)) {
        cartDropdown.classList.remove('active');
    }
});

// Theme Toggle
if (themeToggle) {
    const savedTheme = localStorage.getItem('theme');

    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }

    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');

        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            localStorage.setItem('theme', 'light');
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        }
    });
}

// Navbar Scroll Effect
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    if (!navbar) return;

    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Back to Top
if (backToTop) {
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTop.classList.add('show');
        } else {
            backToTop.classList.remove('show');
        }
    });

    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Quote Buttons
document.querySelectorAll('.btn-quote').forEach(btn => {
    btn.addEventListener('click', function () {
        const product = this.dataset.product || 'this product';
        showToast(`Enquiry sent for ${product}!`);
    });
});

// Enquiry Form
const enquiryForm = document.getElementById('quickEnquiryForm');

if (enquiryForm) {
    enquiryForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const name = document.getElementById('enqName')?.value;
        const email = document.getElementById('enqEmail')?.value;

        if (name && email) {
            showToast('✅ Enquiry sent successfully!');
            this.reset();
        } else {
            showToast('⚠️ Please fill all fields!', 'error');
        }
    });
}

// Live Chat
const liveChat = document.querySelector('.live-chat');

if (liveChat) {
    liveChat.addEventListener('click', () => {
        showToast('💬 Connecting to support...');
    });
}

// Cart Demo Count
let cartCount = 0;
const cartCountSpan = document.querySelector('.cart-count');

const addToCartDemo = () => {
    cartCount++;
    if (cartCountSpan) cartCountSpan.textContent = cartCount;
    showToast('Product added!');
};

document.querySelectorAll('.btn-quote').forEach(btn => {
    btn.addEventListener('click', addToCartDemo);
});