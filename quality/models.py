from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Quality(models.Model):

    RESULT_CHOICES = [
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
    ]

    # --- Basic info ---
    batch_id = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Batch identifier for traceability",
    )

    # --- Quality parameters ---
    mfi = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Melt Flow Index",
    )
    density = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.000'))],
        help_text="Density in g/cm³",
    )
    moisture = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Moisture percentage",
    )

    # --- Result ---
    qc_result = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES,
        db_index=True,
    )

    # --- Date ---
    test_date = models.DateField(db_index=True)

    # --- Timestamp ---
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-test_date', '-id']
        verbose_name = 'Quality Record'
        verbose_name_plural = 'Quality Records'
        indexes = [
            models.Index(fields=['qc_result']),
            models.Index(fields=['test_date']),
        ]

    def __str__(self):
        return f"{self.batch_id} — {self.qc_result}"