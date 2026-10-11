from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal


class Finance(models.Model):

    TRANSACTION_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    CATEGORY_CHOICES = [
        ('Raw Material', 'Raw Material'),
        ('Salary', 'Salary'),
        ('Transport', 'Transport'),
        ('Maintenance', 'Maintenance'),
        ('Sales', 'Sales'),
        ('Electricity', 'Electricity'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=150)
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_CHOICES
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    description = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.localdate)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Completed'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-id']
        verbose_name = 'Finance Record'
        verbose_name_plural = 'Finance Records'
        indexes = [
            models.Index(fields=['transaction_type', 'status']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.title} — ₹{self.amount}"