
    document.addEventListener("DOMContentLoaded", function () {
        const elements = document.querySelectorAll(".animate-on-scroll");

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = "1";
                    entry.target.style.transform = "translateY(0)";
                    entry.target.style.transition = "all 0.6s ease";
                }
            });
        }, { threshold: 0.2 });

        elements.forEach(el => observer.observe(el));
    });

    // Back to Top Button Functionality
    document.addEventListener("DOMContentLoaded", function() {
        const backToTopButton = document.getElementById('backToTop');
        
        if (backToTopButton) {
            window.addEventListener('scroll', function() {
                if (window.pageYOffset > 300) {
                    backToTopButton.classList.add('show');
                } else {
                    backToTopButton.classList.remove('show');
                }
            });
            
            backToTopButton.addEventListener('click', function() {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
    });

    // Newsletter subscription animation
    document.addEventListener("DOMContentLoaded", function() {
        const newsletterBtn = document.querySelector('.newsletter-form button');
        const newsletterInput = document.querySelector('.newsletter-form input');
        
        if (newsletterBtn && newsletterInput) {
            newsletterBtn.addEventListener('click', function() {
                const email = newsletterInput.value;
                if (email && email.includes('@')) {
                    alert('Thank you for subscribing to our newsletter!');
                    newsletterInput.value = '';
                    newsletterInput.style.borderColor = '#4caf50';
                    setTimeout(() => {
                        newsletterInput.style.borderColor = '';
                    }, 2000);
                } else if (email) {
                    alert('Please enter a valid email address.');
                    newsletterInput.style.borderColor = '#f44336';
                    setTimeout(() => {
                        newsletterInput.style.borderColor = '';
                    }, 2000);
                } else {
                    newsletterInput.style.borderColor = '#f44336';
                    setTimeout(() => {
                        newsletterInput.style.borderColor = '';
                    }, 2000);
                }
            });
        }
    });
    // Navbar Scroll Effect - Add this to your existing script
window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Add hover sound effect (optional - remove if not needed)
// This adds a subtle animation to navbar items
const navLinks = document.querySelectorAll('nav ul li a');
navLinks.forEach(link => {
    link.addEventListener('mouseenter', function(e) {
        this.style.transition = 'all 0.3s ease';
    });
});
    