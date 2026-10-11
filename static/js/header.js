/* topbar.js — phone aur email links ko sahi chalana */
(function () {
  'use strict';

  var isDesktop = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* EMAIL
     Mobile  : mailto: (phone ka mail/Gmail app khulta hai)
     Desktop : Gmail compose browser me khulta hai (mailto ka error nahi aata) */
  document.querySelectorAll('[data-email]').forEach(function (a) {
    if (!isDesktop) return;
    var to = encodeURIComponent(a.getAttribute('data-email'));
    a.href = 'https://mail.google.com/mail/?view=cm&fs=1&to=' + to + '&su=' + encodeURIComponent('Product Enquiry');
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
  });

  /* PHONE
     Mobile  : tel: seedha dialer kholta hai
     Desktop : laptop pe call app nahi hota, isliye number copy hota hai */
  var toast;
  function showToast(msg) {
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'site-toast';
      toast.setAttribute('role', 'status');
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(showToast.t);
    showToast.t = setTimeout(function () { toast.classList.remove('show'); }, 2200);
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      var t = document.createElement('textarea');
      t.value = text; t.style.position = 'fixed'; t.style.opacity = '0';
      document.body.appendChild(t); t.select();
      try { document.execCommand('copy') ? resolve() : reject(); } catch (e) { reject(e); }
      document.body.removeChild(t);
    });
  }

  if (isDesktop) {
    document.querySelectorAll('[data-phone]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var num = a.getAttribute('data-phone');
        copyText(num).then(
          function () { showToast('Number copied: ' + num); },
          function () { showToast('Call us: ' + num); }
        );
      });
    });
  }
})();
