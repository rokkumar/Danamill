from django.db import models
from django.core.validators import MinValueValidator


class Dispatch(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
    ]

    # --- Basic info ---
    dispatch_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique identifier for this dispatch",
    )
    customer_name = models.CharField(max_length=150)
    product_name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantity (must be 1 or more)",
    )

    # --- Transport ---
    vehicle_number = models.CharField(max_length=50, blank=True)
    driver_name = models.CharField(max_length=100, blank=True)

    # --- Status ---
    dispatch_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending',
    )

    # --- Date ---
    dispatch_date = models.DateField()

    # --- Timestamp ---
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-dispatch_date', '-id']
        verbose_name = 'Dispatch Record'
        verbose_name_plural = 'Dispatch Records'
        indexes = [
            models.Index(fields=['dispatch_status']),
            models.Index(fields=['dispatch_date']),
        ]

    def __str__(self):
        return f"{self.dispatch_id} — {self.customer_name}"