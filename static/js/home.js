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




/* ========== ANKUSH PATEL - CTA + ENQUIRY SECTION (FIXED) ========== */


(() => {
    'use strict';

    function initAOS() {
        if (typeof AOS !== 'undefined') {
            AOS.init({ duration: 1000, once: true });
        }
    }

    function initHeaderInteractions() {
        const mobileToggle = document.getElementById('mobileToggle');
        const navMenu = document.getElementById('navMenu');
        const mobileOverlay = document.getElementById('mobileOverlay');
        const searchToggle = document.getElementById('searchToggle');
        const searchDropdown = document.getElementById('searchDropdown');
        const cartBtn = document.getElementById('cartBtn');
        const cartDropdown = document.getElementById('cartDropdown');
        const themeToggle = document.getElementById('themeToggle');
        const backToTop = document.getElementById('backToTopFooter');

        if (mobileToggle && navMenu) {
            mobileToggle.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                if (mobileOverlay) {
                    mobileOverlay.classList.toggle('active');
                }
                document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
            });
        }

        if (mobileOverlay) {
            mobileOverlay.addEventListener('click', () => {
                if (navMenu) {
                    navMenu.classList.remove('active');
                }
                mobileOverlay.classList.remove('active');
                document.body.style.overflow = '';
            });
        }

        if (searchToggle && searchDropdown) {
            searchToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                searchDropdown.classList.toggle('active');
                if (cartDropdown) {
                    cartDropdown.classList.remove('active');
                }
            });
        }

        if (cartBtn && cartDropdown) {
            cartBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                cartDropdown.classList.toggle('active');
                if (searchDropdown) {
                    searchDropdown.classList.remove('active');
                }
            });
        }

        document.addEventListener('click', (e) => {
            if (searchDropdown && searchToggle && !searchDropdown.contains(e.target) && !searchToggle.contains(e.target)) {
                searchDropdown.classList.remove('active');
            }
            if (cartDropdown && cartBtn && !cartDropdown.contains(e.target) && !cartBtn.contains(e.target)) {
                cartDropdown.classList.remove('active');
            }
        });

        if (themeToggle) {
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'dark') {
                document.body.classList.add('dark-mode');
                themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            }

            themeToggle.addEventListener('click', () => {
                document.body.classList.toggle('dark-mode');
                const darkModeEnabled = document.body.classList.contains('dark-mode');
                localStorage.setItem('theme', darkModeEnabled ? 'dark' : 'light');
                themeToggle.innerHTML = darkModeEnabled ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
            });
        }

        const navbar = document.querySelector('.navbar');
        window.addEventListener('scroll', () => {
            if (navbar) {
                navbar.classList.toggle('scrolled', window.scrollY > 50);
            }
        });

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
    }

    class ToastManager {
        constructor(container) {
            this.container = container;
            this.timerMap = new WeakMap();
        }

        push(message, type = 'success', duration = 4500) {
            if (!this.container) {
                return;
            }

            const toast = document.createElement('div');
            toast.className = `toast-notification ${type === 'success' ? 'toast-success' : 'toast-error'}`;
            toast.setAttribute('role', type === 'error' ? 'alert' : 'status');
            toast.setAttribute('aria-atomic', 'true');
            toast.innerHTML = `
                <span class="toast-icon" aria-hidden="true">${type === 'success' ? 'OK' : '!'}</span>
                <span class="toast-text">${message}</span>
                <button type="button" class="toast-close" aria-label="Close notification">x</button>
            `;

            const closeBtn = toast.querySelector('.toast-close');
            closeBtn?.addEventListener('click', () => this.remove(toast));

            this.container.appendChild(toast);
            const timer = window.setTimeout(() => this.remove(toast), duration);
            this.timerMap.set(toast, timer);
        }

        remove(toast) {
            if (!toast || !toast.parentElement) {
                return;
            }
            const timer = this.timerMap.get(toast);
            if (timer) {
                window.clearTimeout(timer);
            }
            toast.classList.add('is-leaving');
            window.setTimeout(() => {
                toast.remove();
            }, 260);
        }
    }

    class EnquiryFormController {
        constructor(form, toastManager) {
            this.form = form;
            this.toastManager = toastManager;
            this.submitBtn = form.querySelector('#submitBtn');
            this.formMessage = form.querySelector('#formMessage');
            this.isSubmitting = false;
            this.originalBtnHTML = this.submitBtn ? this.submitBtn.innerHTML : '';
            this.fields = {
                name: form.querySelector('#enquiry_name'),
                email: form.querySelector('#enquiry_email'),
                phone: form.querySelector('#enquiry_phone'),
                product: form.querySelector('#enquiry_product'),
                message: form.querySelector('#enquiry_message'),
            };
        }

        init() {
            this.bindFormSubmit();
            this.bindFieldLiveValidation();
        }

        bindFormSubmit() {
            this.form.addEventListener('submit', (event) => this.handleSubmit(event));
        }

        bindFieldLiveValidation() {
            Object.entries(this.fields).forEach(([fieldName, input]) => {
                if (!input) {
                    return;
                }
                const eventType = input.tagName.toLowerCase() === 'select' ? 'change' : 'input';
                input.addEventListener(eventType, () => {
                    if (input.value.trim()) {
                        this.clearFieldError(fieldName);
                    }
                });
            });
        }

        getCsrfToken() {
            const formToken = this.form.querySelector('[name=csrfmiddlewaretoken]')?.value;
            if (formToken) {
                return formToken;
            }
            const cookieToken = document.cookie
                .split('; ')
                .find((row) => row.startsWith('csrftoken='));
            return cookieToken ? decodeURIComponent(cookieToken.split('=')[1]) : '';
        }

        getPayload() {
            return {
                name: (this.fields.name?.value || '').trim(),
                email: (this.fields.email?.value || '').trim(),
                phone: (this.fields.phone?.value || '').trim(),
                product: (this.fields.product?.value || '').trim(),
                message: (this.fields.message?.value || '').trim(),
            };
        }

        validate(payload) {
            const errors = {};

            if (!payload.name) {
                errors.name = 'Name is required.';
            }
            if (!payload.email) {
                errors.email = 'Email is required.';
            }
            if (!payload.phone) {
                errors.phone = 'Phone is required.';
            }
            if (!payload.product) {
                errors.product = 'Please select a product.';
            }
            return errors;
        }

        clearAllErrors() {
            this.form.querySelectorAll('.input-group').forEach((group) => group.classList.remove('has-error'));
            this.form.querySelectorAll('.error-text').forEach((node) => {
                node.textContent = '';
            });
            Object.values(this.fields).forEach((input) => {
                if (input) {
                    input.removeAttribute('aria-invalid');
                }
            });
        }

        setFieldError(fieldName, message) {
            const input = this.fields[fieldName];
            const errorNode = document.getElementById(`error_${fieldName}`);

            if (input) {
                input.setAttribute('aria-invalid', 'true');
                input.closest('.input-group')?.classList.add('has-error');
            }
            if (errorNode) {
                errorNode.textContent = message;
            }
        }

        clearFieldError(fieldName) {
            const input = this.fields[fieldName];
            const errorNode = document.getElementById(`error_${fieldName}`);
            input?.removeAttribute('aria-invalid');
            input?.closest('.input-group')?.classList.remove('has-error');
            if (errorNode) {
                errorNode.textContent = '';
            }
        }

        focusFirstError(errorMap) {
            const firstField = Object.keys(errorMap)[0];
            if (!firstField) {
                return;
            }
            const input = this.fields[firstField];
            if (!input) {
                return;
            }
            input.focus({ preventScroll: true });
            input.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        setFormFeedback(message, type) {
            if (!this.formMessage) {
                return;
            }
            this.formMessage.textContent = message;
            this.formMessage.classList.remove('success', 'error', 'is-visible', 'feedback-enter');
            if (type) {
                this.formMessage.classList.add(type, 'is-visible');
                requestAnimationFrame(() => this.formMessage?.classList.add('feedback-enter'));
            }
        }

        setLoadingState(isLoading) {
            if (!this.submitBtn) {
                return;
            }

            this.submitBtn.disabled = isLoading;
            this.submitBtn.setAttribute('aria-busy', String(isLoading));

            if (isLoading) {
                this.submitBtn.classList.add('is-loading');
                this.submitBtn.innerHTML = `
                    <span class="btn-spinner" aria-hidden="true"></span>
                    <span>Submitting...</span>
                `;
            } else {
                this.submitBtn.classList.remove('is-loading');
                this.submitBtn.removeAttribute('aria-busy');
                this.submitBtn.innerHTML = this.originalBtnHTML;
            }
        }

        applyErrors(errorMap, fallbackMessage) {
            Object.entries(errorMap).forEach(([field, message]) => {
                this.setFieldError(field, String(message));
            });
            this.focusFirstError(errorMap);
            this.setFormFeedback(fallbackMessage || 'Please correct the highlighted fields.', 'error');
        }

        async parseResponseJson(response) {
            try {
                return await response.json();
            } catch (error) {
                return null;
            }
        }

        resetAfterSuccess() {
            this.form.reset();
            this.clearAllErrors();
            const nameField = this.fields.name;
            if (nameField) {
                nameField.focus({ preventScroll: true });
            }
        }

        async handleSubmit(event) {
            event.preventDefault();
            if (this.isSubmitting) {
                return;
            }

            this.clearAllErrors();
            this.setFormFeedback('', null);

            const payload = this.getPayload();
            const clientErrors = this.validate(payload);
            if (Object.keys(clientErrors).length > 0) {
                this.applyErrors(clientErrors, 'Please fill all required fields.');
                this.toastManager.push('Please fix the highlighted errors.', 'error');
                return;
            }

            this.isSubmitting = true;
            this.setLoadingState(true);

            try {
                const response = await fetch(this.form.action, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken(),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: JSON.stringify(payload),
                });

                const result = await this.parseResponseJson(response);

                if (!result || !response.ok || !result.success) {
                    const backendErrors = result?.errors && typeof result.errors === 'object' ? result.errors : {};
                    const message = result?.message || 'Unable to submit enquiry right now.';
                    if (Object.keys(backendErrors).length) {
                        this.applyErrors(backendErrors, message);
                    } else {
                        this.setFormFeedback(message, 'error');
                    }
                    this.toastManager.push(message, 'error');
                    return;
                }

                const successMessage = result.message || 'Enquiry submitted successfully! We will contact you soon.';
                this.setFormFeedback(successMessage, 'success');
                this.toastManager.push(successMessage, 'success');
                this.resetAfterSuccess();
            } catch (error) {
                const networkMessage = 'Network issue. Please try again in a moment.';
                this.setFormFeedback(networkMessage, 'error');
                this.toastManager.push(networkMessage, 'error');
                console.error('Enquiry submission error:', error);
            } finally {
                this.isSubmitting = false;
                this.setLoadingState(false);
            }
        }
    }

    function initQuoteButtons(toastManager) {
        document.querySelectorAll('.btn-quote').forEach((btn) => {
            btn.addEventListener('click', function () {
                const product = this.dataset.product || 'this product';
                toastManager.push(`Enquiry started for ${product}.`, 'success');
            });
        });
    }

    function initEnquiryForm() {
        const form = document.getElementById('quickEnquiryForm');
        if (!form) {
            return;
        }
        const toastContainer = document.getElementById('toastContainer');
        const toastManager = new ToastManager(toastContainer);
        const controller = new EnquiryFormController(form, toastManager);
        controller.init();
        initQuoteButtons(toastManager);
    }

    function boot() {
        initAOS();
        initHeaderInteractions();
        initEnquiryForm();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();



// Khushi Pal...

// Quote Buttons
document.querySelectorAll('.btn-quote').forEach(btn => {
    btn.addEventListener('click', function () {
        const product = this.dataset.product || 'this product';
        showToast(`Enquiry sent for ${product}!`);
    });
});




/// ========================================
// ORDER FORM INTERACTIONS - ENHANCED
// ========================================

```javascript
// ========================================
// PREMIUM ORDER FORM INTERACTIONS
// ========================================

document.addEventListener("DOMContentLoaded", function () {

    const orderForm = document.getElementById("orderForm");

    if (!orderForm) return;

    const inputs = orderForm.querySelectorAll("input, textarea, select");

    // Smooth Focus Animation
    inputs.forEach(input => {

        input.addEventListener("focus", function () {
            this.parentElement.classList.add("active");
        });

        input.addEventListener("blur", function () {
            this.parentElement.classList.remove("active");
        });

    });

    // Form Validation
    orderForm.addEventListener("submit", function (e) {

        let valid = true;

        const requiredFields = [
            "product",
            "quantity",
            "customer_name",
            "email",
            "phone"
        ];

        requiredFields.forEach(name => {
            const field = orderForm.querySelector(`[name="${name}"]`);

            if (field && !field.value.trim()) {
                valid = false;
                field.style.borderColor = "#dc2626";
                field.style.animation = "shake 0.4s ease";

                setTimeout(() => {
                    field.style.animation = "";
                }, 500);
            } else if (field) {
                field.style.borderColor = "#dbe2ea";
            }
        });

        // Email Validation
        const email = orderForm.querySelector('[name="email"]');

        if (email && email.value.trim()) {
            const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!pattern.test(email.value.trim())) {
                valid = false;
                email.style.borderColor = "#dc2626";
                showMessage("Please enter a valid email address");
            }
        }

        if (!valid) {
            e.preventDefault();
            showMessage("Please fill all required fields correctly");
        }

    });

    // Message Box
    function showMessage(message) {
        let box = document.querySelector(".form-message");

        if (!box) {
            box = document.createElement("div");
            box.className = "form-message";
            orderForm.prepend(box);
        }

        box.innerText = message;
        box.style.display = "block";
        box.style.background = "#fee2e2";
        box.style.color = "#b91c1c";
        box.style.padding = "14px";
        box.style.marginBottom = "20px";
        box.style.borderRadius = "12px";
        box.style.textAlign = "center";
        box.style.fontWeight = "500";

        setTimeout(() => {
            box.style.display = "none";
        }, 3000);
    }

});
```

