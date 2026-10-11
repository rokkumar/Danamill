/* reveal.js — sab pages: scroll reveal ([data-rv], [data-stagger]) + number counters ([data-count]) */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('[data-stagger]').forEach(function (parent) {
    Array.prototype.forEach.call(parent.children, function (el, i) {
      el.style.setProperty('--d', (i * 90) + 'ms');
    });
  });

  function runCounter(el) {
    var end = parseInt(el.getAttribute('data-count'), 10);
    if (isNaN(end) || reduce) return;
    var start = null, dur = 1400;
    function tick(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  function reveal(el) {
    el.classList.add('a-in');
    if (el.hasAttribute('data-count')) runCounter(el);
    el.querySelectorAll('[data-count]').forEach(runCounter);
  }

  var targets = document.querySelectorAll('[data-rv], [data-stagger] > *');

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

  window.__revealReady = true;
})();
