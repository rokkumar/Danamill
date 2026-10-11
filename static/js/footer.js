/* footer.js — scroll reveal + back to top */
(function () {
  'use strict';

  /* Reveal */
  var items = document.querySelectorAll('.site-footer .reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        io.unobserve(en.target);
      });
    }, { threshold: 0.15 });
    items.forEach(function (el, i) {
      el.style.transitionDelay = (i * 80) + 'ms';
      io.observe(el);
    });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  /* Back to top */
  var btn = document.getElementById('backToTop');
  if (btn) {
    var toggle = function () { btn.classList.toggle('show', window.scrollY > 400); };
    window.addEventListener('scroll', toggle, { passive: true });
    toggle();
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
})();
