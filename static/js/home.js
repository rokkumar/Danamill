// ========================================
// PLASTICORP - MAIN JAVASCRIPT
// Mobile Menu, Smooth Scroll, Form Handling
// ========================================

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    
    // ========== MOBILE MENU TOGGLE ==========
    const menuToggle = document.getElementById('mobile-menu');
    const mobileNav = document.getElementById('mobile-nav');
    
    if (menuToggle && mobileNav) {
        menuToggle.addEventListener('click', function() {
            mobileNav.classList.toggle('active');
            // Change icon
            const icon = menuToggle.querySelector('i');
            if (mobileNav.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
        
        // Close mobile menu when clicking a link
        const mobileLinks = mobileNav.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileNav.classList.remove('active');
                const icon = menuToggle.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            });
        });
    }
    
    // ========== SMOOTH SCROLL FOR ANCHOR LINKS ==========
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // ========== ACTIVE NAVIGATION ON SCROLL ==========
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navbar a, .mobile-nav a');
    
    window.addEventListener('scroll', function() {
        let current = '';
        const scrollPosition = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href').substring(1);
            if (href === current) {
                link.classList.add('active');
            }
        });
    });
    
    // ========== FORM SUBMISSION ==========
    const enquiryForm = document.getElementById('enquiryForm');
    if (enquiryForm) {
        enquiryForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(enquiryForm);
            const data = Object.fromEntries(formData);
            
            // Show success message (you can replace with actual AJAX submission)
            alert('Thank you for your enquiry! Our team will contact you soon.');
            enquiryForm.reset();
        });
    }
    
    // ========== SCROLL TO TOP BUTTON ==========
    const scrollBtn = document.createElement('div');
    scrollBtn.className = 'scroll-top';
    scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(scrollBtn);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 500) {
            scrollBtn.classList.add('show');
        } else {
            scrollBtn.classList.remove('show');
        }
    });
    
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // ========== DARK MODE TOGGLE ==========
    const darkModeToggle = document.querySelector('.fa-moon');
    let isDarkMode = false;
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            isDarkMode = !isDarkMode;
            if (isDarkMode) {
                document.body.style.background = '#1a1a2e';
                document.body.style.color = '#ffffff';
                darkModeToggle.classList.remove('fa-moon');
                darkModeToggle.classList.add('fa-sun');
            } else {
                document.body.style.background = '#ffffff';
                document.body.style.color = '#333333';
                darkModeToggle.classList.remove('fa-sun');
                darkModeToggle.classList.add('fa-moon');
            }
        });
    }
});

// Add scroll-top styles dynamically
const style = document.createElement('style');
style.textContent = `
    .scroll-top {
        position: fixed;
        bottom: 100px;
        right: 30px;
        background: #1a4a8a;
        color: white;
        width: 45px;
        height: 45px;
        border-radius: 50%;
        display: none;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        font-size: 20px;
        z-index: 999;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .scroll-top.show {
        display: flex;
    }
    .scroll-top:hover {
        background: #0e3a6e;
        transform: translateY(-3px);
    }
`;
document.head.appendChild(style);


// ========== TRUST BADGES COUNTER ANIMATION ==========
const trustItems = document.querySelectorAll('.trust-item span');
const trustObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.5 });

trustItems.forEach(item => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(20px)';
    item.style.transition = 'all 0.6s ease';
    trustObserver.observe(item);
});