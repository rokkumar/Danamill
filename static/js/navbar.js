/* navbar.js — mobile menu, search, cart, dark mode, active link */
(function () {
  'use strict';

  var $ = function (id) { return document.getElementById(id); };
  var body = document.body;

  var header = $('siteHeader');
  var menuBtn = $('menuBtn'), panel = $('mobilePanel'), overlay = $('menuOverlay');
  var searchBtn = $('searchBtn'), searchPanel = $('searchPanel'), searchInput = $('searchInput');
  var cartBtn = $('cartBtn'), cartPanel = $('cartPanel'), cartItems = $('cartItems'), cartCount = $('cartCount');
  var themeBtn = $('themeBtn');

  /* ---------- Mobile menu ---------- */
  function setMenu(open) {
    if (!panel || !menuBtn) return;
    panel.classList.toggle('active', open);
    if (overlay) overlay.classList.toggle('active', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    body.style.overflow = open ? 'hidden' : '';
    if (open) { setDrop(searchBtn, searchPanel, false); setDrop(cartBtn, cartPanel, false); }
  }
  if (menuBtn) menuBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    setMenu(!panel.classList.contains('active'));
  });
  if (overlay) overlay.addEventListener('click', function () { setMenu(false); });
  if (panel) panel.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () { setMenu(false); });
  });

  /* ---------- Search / Cart dropdowns ---------- */
  function setDrop(btn, box, open) {
    if (!btn || !box) return;
    box.classList.toggle('active', open);
    btn.setAttribute('aria-expanded', String(open));
  }

  if (searchBtn && searchPanel) searchBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    var open = !searchPanel.classList.contains('active');
    setMenu(false); setDrop(cartBtn, cartPanel, false); setDrop(searchBtn, searchPanel, open);
    if (open && searchInput) setTimeout(function () { searchInput.focus(); }, 80);
  });

  function esc(v) {
    return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function refreshCart() {
    if (!cartItems) return;
    fetch('/cart/api/dropdown/', { credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        if (d.items && d.items.length) {
          cartItems.innerHTML = d.items.map(function (it) {
            return '<div class="cart-item"><span>' + esc(it.name) + ' × ' + esc(it.qty) +
                   '</span><span>₹' + esc(it.total) + '</span></div>';
          }).join('');
        } else {
          cartItems.textContent = 'No items yet.';
        }
        if (cartCount && d.total_items !== undefined) cartCount.textContent = d.total_items;
      })
      .catch(function () { /* API na ho to bhi header chalta rahe */ });
  }

  if (cartBtn && cartPanel) cartBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    var open = !cartPanel.classList.contains('active');
    setMenu(false); setDrop(searchBtn, searchPanel, false); setDrop(cartBtn, cartPanel, open);
    if (open) refreshCart();
  });

  [searchPanel, cartPanel].forEach(function (p) {
    if (p) p.addEventListener('click', function (e) { e.stopPropagation(); });
  });

  document.addEventListener('click', function () {
    setDrop(searchBtn, searchPanel, false);
    setDrop(cartBtn, cartPanel, false);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    setMenu(false); setDrop(searchBtn, searchPanel, false); setDrop(cartBtn, cartPanel, false);
  });

  /* ---------- Dark mode ---------- */
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var dark = body.classList.toggle('dark-mode');
    try { localStorage.setItem('theme', dark ? 'dark' : 'light'); } catch (e) {}
  });

  /* ---------- Resize + scroll shadow ---------- */
  window.addEventListener('resize', function () { if (window.innerWidth > 992) setMenu(false); });
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 10); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Active link ---------- */
  var path = location.pathname.replace(/\/+$/, '') || '/';
  document.querySelectorAll('.nav-link, .m-link[href], .m-sub a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) === '#') return;
    var u = new URL(href, location.origin);
    if (u.search) return;                       // ?cat=... wale items ko skip
    var p = u.pathname.replace(/\/+$/, '') || '/';
    if (p === path || (p !== '/' && path.indexOf(p + '/') === 0)) a.classList.add('active');
  });

  refreshCart();
})();
