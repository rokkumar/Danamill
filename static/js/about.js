/* about.js — scroll reveal + number counters */
(function () {
  'use strict';

  var root = document.querySelector('.about-page');
  if (!root) return;

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* stagger delay (children ko ek-ek karke) */
  root.querySelectorAll('[data-stagger]').forEach(function (parent) {
    Array.prototype.forEach.call(parent.children, function (el, i) {
      el.style.setProperty('--d', (i * 90) + 'ms');
    });
  });

  /* counters */
  function runCounter(el) {
    var end = parseInt(el.getAttribute('data-count'), 10);
    if (isNaN(end) || reduce) { el.textContent = end; return; }
    var dur = 1400, start = null;
    function tick(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(end * eased);
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  var targets = root.querySelectorAll('[data-rv], [data-stagger] > *');

  function reveal(el) {
    el.classList.add('a-in');
    el.querySelectorAll('[data-count]').forEach(runCounter);
  }

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        reveal(en.target);
        io.unobserve(en.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    targets.forEach(function (el) { io.observe(el); });
  } else {
    targets.forEach(reveal);
  }

  window.__aboutReady = true;
})();
