from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal


class Event(models.Model):
    """An event or project (e.g., Ganesh Navratri 2026)."""

    name = models.CharField(
        max_length=200,
        help_text="e.g. Ganesh Navratri 2026",
    )
    description = models.CharField(
        max_length=300,
        blank=True,
        help_text="Short subtitle or description",
    )
    total_collection = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Total funds collected for this event",
    )
    start_date = models.DateField(default=timezone.localdate)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', '-id']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.name

    # --------- Aggregated stats ----------
    def total_expenses(self):
        result = self.items.aggregate(
            t=models.Sum('total_cost')
        )['t']
        return result or Decimal('0.00')

    def total_paid(self):
        result = self.items.aggregate(
            t=models.Sum('paid_amount')
        )['t']
        return result or Decimal('0.00')

    def total_pending(self):
        return self.total_expenses() - self.total_paid()

    def remaining_funds(self):
        return self.total_collection - self.total_paid()


class EventItem(models.Model):
    """A single expense item in an event (e.g., Decoration ₹13,000)."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='items',
    )
    item_name = models.CharField(
        max_length=200,
        help_text="e.g. Decoration, Tent house, Ganesh idol",
    )
    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    notes = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Event Item'
        verbose_name_plural = 'Event Items'

    def __str__(self):
        return f"{self.item_name} — ₹{self.total_cost}"

    def pending_amount(self):
        return self.total_cost - self.paid_amount

    def is_fully_paid(self):
        return self.pending_amount() <= 0