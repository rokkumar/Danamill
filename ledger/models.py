from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal


class Client(models.Model):
    """A customer who buys granules from us."""

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Balance carried forward from previous period",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.name

    def total_sales(self):
        result = self.entries.filter(entry_type='SALE').aggregate(
            t=models.Sum('amount')
        )['t']
        return result or Decimal('0.00')

    def total_payments(self):
        result = self.entries.filter(entry_type='PAYMENT').aggregate(
            t=models.Sum('payment_amount')
        )['t']
        return result or Decimal('0.00')

    def outstanding(self):
        return self.opening_balance + self.total_sales() - self.total_payments()


class LedgerEntry(models.Model):
    """One row of the ledger — either a sale or a payment."""

    ENTRY_TYPE_CHOICES = [
        ('SALE', 'Sale (Material Given)'),
        ('PAYMENT', 'Payment Received'),
    ]

    PAY_TYPE_CHOICES = [
        ('CASH', 'Cash'),
        ('PH', 'PhonePe / Online'),
        ('CHEQUE', 'Cheque'),
        ('NEFT', 'NEFT / RTGS'),
        ('OTHER', 'Other'),
    ]

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='entries'
    )
    entry_type = models.CharField(
        max_length=10, choices=ENTRY_TYPE_CHOICES, default='SALE'
    )

    # ---------- Sale columns ----------
    date = models.DateField(default=timezone.localdate)
    bill_no = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00')
    )

    # ---------- Payment columns ----------
    payment_date = models.DateField(blank=True, null=True)
    payment_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    pay_type = models.CharField(
        max_length=10, choices=PAY_TYPE_CHOICES, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'id']
        verbose_name = 'Ledger Entry'
        verbose_name_plural = 'Ledger Entries'
        indexes = [
            models.Index(fields=['client', 'date']),
            models.Index(fields=['client', 'payment_date']),
        ]

    def __str__(self):
        return f"{self.client.name} — {self.date} — {self.entry_type}"

    def save(self, *args, **kwargs):
        # Amount is always derived from quantity × rate for SALE rows
        if self.entry_type == 'SALE':
            if self.quantity and self.rate:
                self.amount = self.quantity * self.rate
            self.payment_amount = Decimal('0.00')
            self.pay_type = None
            self.payment_date = None
        else:
            # For PAYMENT rows — sale fields cleared
            self.quantity = Decimal('0.00')
            self.rate = Decimal('0.00')
            self.amount = Decimal('0.00')
            self.bill_no = None
            if not self.payment_date:
                self.payment_date = self.date
        super().save(*args, **kwargs)

    def effective_date(self):
        """The date this row should be placed on the timeline."""
        if self.entry_type == 'PAYMENT' and self.payment_date:
            return self.payment_date
        return self.date

    @property
    def signed_amount(self):
        """Positive for SALE, negative for PAYMENT — used for running balance."""
        if self.entry_type == 'SALE':
            return self.amount
        return -self.payment_amount