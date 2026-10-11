/* contact.js — form validation + AJAX submit, character counter, business-hours "Open now" badge */
(function () {
  'use strict';

  var form = document.getElementById('contactForm');
  if (!form) return;

  var box = document.getElementById('contactMessage');
  var btn = document.getElementById('submitContactBtn');
  var label = btn.querySelector('.btn-label');
  var area = document.getElementById('contact_message');
  var counter = document.getElementById('messageCount');
  var defaultLabel = label.textContent;
  var FIELDS = ['name', 'email', 'phone', 'subject', 'message'];

  /* ---------- helpers ---------- */
  function getCookie(name) {
    var m = document.cookie.match('(?:^|; )' + name + '=([^;]*)');
    return m ? decodeURIComponent(m[1]) : '';
  }

  function showMessage(type, text) {
    box.textContent = text;
    box.className = 'form-message' + (type ? ' ' + type : '');
    if (type) box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function setError(field, msg) {
    var input = form.elements[field];
    var out = document.getElementById('error_' + field);
    if (out) out.textContent = msg || '';
    if (input) {
      if (msg) input.setAttribute('aria-invalid', 'true');
      else input.removeAttribute('aria-invalid');
    }
  }

  function clearErrors() { FIELDS.forEach(function (f) { setError(f, ''); }); }

  /* ---------- validation ---------- */
  var RULES = {
    name: function (v) {
      if (!v) return 'Please enter your name.';
      if (v.length < 2) return 'Name is too short.';
    },
    email: function (v) {
      if (!v) return 'Please enter your email.';
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return 'Enter a valid email address.';
    },
    phone: function (v) {
      var digits = v.replace(/\D/g, '');
      if (!v) return 'Please enter your phone number.';
      if (!/^[0-9+\-\s()]+$/.test(v) || digits.length < 10 || digits.length > 13) return 'Enter a valid phone number (10 digits).';
    },
    subject: function (v) {
      if (!v) return 'Please enter a subject.';
      if (v.length < 3) return 'Subject is too short.';
    },
    message: function (v) {
      if (!v) return 'Please write your message.';
      if (v.length < 10) return 'Message should be at least 10 characters.';
    }
  };

  function validate() {
    var firstBad = null;
    FIELDS.forEach(function (f) {
      var input = form.elements[f];
      var msg = RULES[f](input.value.trim());
      setError(f, msg);
      if (msg && !firstBad) firstBad = input;
    });
    if (firstBad) firstBad.focus();
    return !firstBad;
  }

  /* validate on leaving a field + clear error while typing */
  FIELDS.forEach(function (f) {
    var input = form.elements[f];
    input.addEventListener('blur', function () {
      if (input.value.trim() !== '') setError(f, RULES[f](input.value.trim()));
    });
    input.addEventListener('input', function () {
      if (input.getAttribute('aria-invalid') === 'true') setError(f, RULES[f](input.value.trim()));
    });
  });

  /* ---------- counter ---------- */
  function updateCount() {
    if (counter && area) counter.textContent = area.value.length + ' / ' + (area.maxLength > 0 ? area.maxLength : 2000);
  }
  if (area) { area.addEventListener('input', updateCount); updateCount(); }

  /* ---------- submit ---------- */
  function setLoading(on) {
    btn.disabled = on;
    btn.classList.toggle('loading', on);
    label.textContent = on ? 'Sending...' : defaultLabel;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    showMessage('', '');
    clearErrors();

    if (!validate()) {
      showMessage('error', 'Please correct the highlighted fields.');
      return;
    }

    /* bot ne honeypot bhara ho to chup-chap success dikha do */
    if (form.elements.website && form.elements.website.value) {
      showMessage('success', 'Thank you! We will contact you soon.');
      form.reset(); updateCount();
      return;
    }

    setLoading(true);

    var ctrl = new AbortController();
    var timer = setTimeout(function () { ctrl.abort(); }, 20000);

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      credentials: 'same-origin',
      signal: ctrl.signal,
      headers: { 'X-CSRFToken': getCookie('csrftoken'), 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json' }
    })
      .then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (data) { return { ok: res.ok, status: res.status, data: data }; });
      })
      .then(function (r) {
        if (r.ok && r.data.success !== false) {
          showMessage('success', r.data.message || 'Message sent successfully! We will contact you soon.');
          form.reset(); updateCount();
          return;
        }
        var errs = r.data.errors || {};
        Object.keys(errs).forEach(function (f) { setError(f, [].concat(errs[f]).join(' ')); });
        var fallback = r.status === 403
          ? 'Session expired. Please refresh the page and try again.'
          : 'Could not send your message. Please check the form or call us directly.';
        showMessage('error', r.data.message || fallback);
      })
      .catch(function (err) {
        showMessage('error', err && err.name === 'AbortError'
          ? 'The request took too long. Please try again.'
          : 'Network issue. Please try again, or contact us on WhatsApp.');
      })
      .then(function () { clearTimeout(timer); setLoading(false); });
  });

  /* ---------- business hours: Open now / Closed now (IST) ---------- */
  (function hours() {
    var card = document.getElementById('hoursCard');
    var badge = document.getElementById('openBadge');
    if (!card || !badge || !window.Intl || !Intl.DateTimeFormat) return;

    var parts;
    try {
      parts = new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Kolkata', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' }).formatToParts(new Date());
    } catch (e) { return; }

    var o = {};
    parts.forEach(function (p) { o[p.type] = p.value; });
    var day = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 }[o.weekday];
    var mins = (parseInt(o.hour, 10) % 24) * 60 + parseInt(o.minute, 10);
    if (day === undefined || isNaN(mins)) return;

    var open = false;
    if (day >= 1 && day <= 5) open = mins >= 9 * 60 && mins < 18 * 60;
    else if (day === 6) open = mins >= 9 * 60 && mins < 14 * 60;

    card.querySelectorAll('li[data-days]').forEach(function (li) {
      if (li.getAttribute('data-days').split(',').indexOf(String(day)) !== -1) li.classList.add('today');
    });

    badge.textContent = open ? 'Open now' : 'Closed now';
    badge.className = 'open-badge ' + (open ? 'is-open' : 'is-closed');
    badge.hidden = false;
  })();
})();
