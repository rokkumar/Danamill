// ============================================================
// JAI DURGA PLASTIC – HOME PAGE JAVASCRIPT
// ============================================================

document.addEventListener('DOMContentLoaded', function() {

    // ============================================================
    // 1. ENQUIRY FORM HANDLING (AJAX with CSRF)
    // ============================================================

    const enquiryForm = document.getElementById('quickEnquiryForm');
    const formMessage = document.getElementById('formMessage');
    const submitButton = document.getElementById('submitBtn');
    const toastContainer = document.getElementById('toastContainer');

    function getCookie(name) {
        const cookies = document.cookie ? document.cookie.split(';') : [];
        for (const cookie of cookies) {
            const trimmedCookie = cookie.trim();
            if (trimmedCookie.startsWith(name + '=')) {
                return decodeURIComponent(trimmedCookie.slice(name.length + 1));
            }
        }
        return '';
    }

    function setMessage(type, text) {
        if (!formMessage) return;
        formMessage.textContent = text;
        formMessage.className = `form-message ${type} is-visible`;
    }

    function clearErrors() {
        if (!enquiryForm) return;
        enquiryForm.querySelectorAll('.input-group.has-error').forEach(group => {
            group.classList.remove('has-error');
        });
        enquiryForm.querySelectorAll('.error-text').forEach(error => {
            error.textContent = '';
        });
    }

    function setFieldErrors(errors) {
        if (!enquiryForm || !errors) return;
        Object.entries(errors).forEach(([field, message]) => {
            const input = enquiryForm.querySelector(`[name="${field}"]`);
            const error = document.getElementById(`error_${field}`);
            if (input) {
                input.closest('.input-group')?.classList.add('has-error');
            }
            if (error) {
                error.textContent = message;
            }
        });
    }

    function showToast(type, text) {
        if (!toastContainer) return;
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        toast.innerHTML = `
            <span class="toast-icon">${type === 'success' ? '✓' : '!'}</span>
            <span class="toast-text">${text}</span>
            <button type="button" class="toast-close" aria-label="Close notification">&times;</button>
        `;
        toastContainer.appendChild(toast);

        const removeToast = () => {
            toast.classList.add('is-leaving');
            setTimeout(() => toast.remove(), 260);
        };

        toast.querySelector('.toast-close')?.addEventListener('click', removeToast);
        setTimeout(removeToast, 4500);
    }

    if (enquiryForm) {
        enquiryForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            clearErrors();
            setMessage('', '');

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.classList.add('is-loading');
                submitButton.innerHTML = '<span class="btn-spinner"></span> Sending...';
            }

            try {
                const response = await fetch(enquiryForm.action, {
                    method: 'POST',
                    body: new FormData(enquiryForm),
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                const data = await response.json();

                if (!response.ok || !data.success) {
                    setFieldErrors(data.errors);
                    setMessage('error', data.message || 'Please check the form and try again.');
                    showToast('error', data.message || 'Please check the form and try again.');
                    return;
                }

                enquiryForm.reset();
                setMessage('success', data.message || 'Enquiry submitted successfully.');
                showToast('success', data.message || 'Enquiry submitted successfully.');
            } catch (error) {
                setMessage('error', 'Network issue. Please try again.');
                showToast('error', 'Network issue. Please try again.');
            } finally {
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.classList.remove('is-loading');
                    submitButton.innerHTML = 'Send Enquiry <i class="fas fa-paper-plane"></i>';
                }
            }
        });
    }

    // ============================================================
    // 2. SCROLL REVEAL ANIMATIONS (Intersection Observer)
    // ============================================================

    const revealItems = document.querySelectorAll(
        '.intro-grid, .product-card, .feature-card, .cta-content-block, .enquiry-form-block'
    );
    if ('IntersectionObserver' in window) {
        revealItems.forEach(item => item.classList.add('home-reveal'));
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });
        revealItems.forEach(item => observer.observe(item));
    } else {
        revealItems.forEach(item => item.classList.add('is-visible'));
    }

    console.log('✅ Home page JS loaded – form ready.');
});