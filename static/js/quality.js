/* quality.js — FAQ accordion (ek time par ek open, keyboard + aria ke saath) */
(function () {
  'use strict';

  var list = document.getElementById('faqList');
  if (!list) return;

  var items = list.querySelectorAll('.faq-item');

  function setOpen(item, open) {
    item.classList.toggle('open', open);
    var btn = item.querySelector('.faq-q');
    if (btn) btn.setAttribute('aria-expanded', String(open));
  }

  items.forEach(function (item) {
    var btn = item.querySelector('.faq-q');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var willOpen = !item.classList.contains('open');
      items.forEach(function (other) { setOpen(other, false); });
      setOpen(item, willOpen);
    });
  });

  /* pehla sawal shuru se khula */
  if (items.length) setOpen(items[0], true);
})();
