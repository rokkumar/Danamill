document.addEventListener("DOMContentLoaded", function () {
    // Scroll animations
    const elements = document.querySelectorAll(".animate-on-scroll");
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
                entry.target.style.transition = "all 0.6s ease";
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });
    elements.forEach(el => observer.observe(el));

    // Back to top
    const backToTop = document.getElementById('backToTop');
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

    // Newsletter
    const subscribeBtn = document.getElementById('newsletterSubscribe');
    const emailInput = document.getElementById('newsletterEmail');
    if (subscribeBtn && emailInput) {
        subscribeBtn.addEventListener('click', () => {
            const email = emailInput.value.trim();
            if (email && email.includes('@')) {
                alert('Thank you for subscribing to our newsletter!');
                emailInput.value = '';
                emailInput.style.borderColor = '#4caf50';
                setTimeout(() => emailInput.style.borderColor = '', 2000);
            } else {
                alert('Please enter a valid email address.');
                emailInput.style.borderColor = '#f44336';
                setTimeout(() => emailInput.style.borderColor = '', 2000);
            }
        });
    }
});