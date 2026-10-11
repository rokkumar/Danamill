/* ============================================================
   Finance — Income page
   ============================================================ */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {

        // Fade in cards
        var cards = document.querySelectorAll('.summary-card, .finance-card');
        cards.forEach(function (card, index) {
            card.style.opacity = '0';
            card.style.transform = 'translateY(15px)';
            setTimeout(function () {
                card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 90);
        });

        // Auto-focus the title input
        var titleInput = document.querySelector('input[name="title"]');
        if (titleInput) titleInput.focus();

        // Block negative amount typing
        var amountInput = document.querySelector('input[name="amount"]');
        if (amountInput) {
            amountInput.addEventListener('input', function () {
                if (parseFloat(this.value) < 0) this.value = '';
            });
        }
    });
})();