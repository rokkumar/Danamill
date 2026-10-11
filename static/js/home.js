// ============================================================
// JAI DURGA PLASTIC – HOME PAGE SCRIPT
// ============================================================

document.addEventListener('DOMContentLoaded', function() {

    // ---------------------------------------------------------
    // Enquiry form (AJAX submit)
    // ---------------------------------------------------------
    var enquiryForm = document.getElementById('quickEnquiryForm');
    var formMessage = document.getElementById('formMessage');
    var submitBtn = document.getElementById('submitBtn');
    var toastBox = document.getElementById('toastContainer');

    function getCookie(name) {
        var cookies = document.cookie ? document.cookie.split(';') : [];
        for (var i = 0; i < cookies.length; i++) {
            var c = cookies[i].trim();
            if (c.indexOf(name + '=') === 0) {
                return decodeURIComponent(c.slice(name.length + 1));
            }
        }
        return '';
    }

    function showToast(type, text) {
        if (!toastBox) return;
        var el = document.createElement('div');
        el.className = 'toast-notification toast-' + type;
        el.innerHTML =
            '<span class="toast-icon">' + (type === 'success' ? '✓' : '!') + '</span>' +
            '<span class="toast-text">' + text + '</span>' +
            '<button type="button" class="toast-close">&times;</button>';
        toastBox.appendChild(el);

        function remove() {
            el.classList.add('is-leaving');
            setTimeout(function() { el.remove(); }, 260);
        }
        el.querySelector('.toast-close').addEventListener('click', remove);
        setTimeout(remove, 4500);
    }

    function clearErrors() {
        if (!enquiryForm) return;
        enquiryForm.querySelectorAll('.has-error').forEach(function(g) {
            g.classList.remove('has-error');
        });
        enquiryForm.querySelectorAll('.error-text').forEach(function(e) {
            e.textContent = '';
        });
    }

    function showFieldErrors(errors) {
        if (!errors) return;
        Object.keys(errors).forEach(function(field) {
            var input = enquiryForm.querySelector('[name="' + field + '"]');
            var errEl = document.getElementById('error_' + field);
            if (input && input.closest('.input-group')) {
                input.closest('.input-group').classList.add('has-error');
            }
            if (errEl) errEl.textContent = errors[field];
        });
    }

    if (enquiryForm) {
        enquiryForm.addEventListener('submit', function(e) {
            e.preventDefault();
            clearErrors();
            if (formMessage) {
                formMessage.textContent = '';
                formMessage.className = 'form-message';
            }
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = 'Sending...';
            }

            fetch(enquiryForm.action, {
                method: 'POST',
                body: new FormData(enquiryForm),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (!data.success) {
                    showFieldErrors(data.errors);
                    if (formMessage) {
                        formMessage.textContent = data.message || 'Please fix the errors.';
                        formMessage.className = 'form-message error is-visible';
                    }
                    showToast('error', data.message || 'Please check the form.');
                    return;
                }
                enquiryForm.reset();
                if (formMessage) {
                    formMessage.textContent = data.message || 'Enquiry submitted.';
                    formMessage.className = 'form-message success is-visible';
                }
                showToast('success', data.message || 'Enquiry submitted.');
            })
            .catch(function() {
                showToast('error', 'Network issue. Please try again.');
            })
            .finally(function() {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = 'Send Enquiry <i class="fas fa-paper-plane"></i>';
                }
            });
        });
    }

    // ---------------------------------------------------------
    // Scroll reveal
    // ---------------------------------------------------------
    var items = document.querySelectorAll(
        '.intro-grid, .product-card, .feature-card, .cta-content-block, .enquiry-form-block'
    );
    if ('IntersectionObserver' in window && items.length) {
        items.forEach(function(i) { i.classList.add('home-reveal'); });
        var obs = new IntersectionObserver(function(entries) {
            entries.forEach(function(en) {
                if (en.isIntersecting) {
                    en.target.classList.add('is-visible');
                    obs.unobserve(en.target);
                }
            });
        }, { threshold: 0.12 });
        items.forEach(function(i) { obs.observe(i); });
    }
});