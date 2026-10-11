from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Machine(models.Model):

    STATUS_CHOICES = [
        ('Running', 'Running'),
        ('Idle', 'Idle'),
        ('Breakdown', 'Breakdown'),
    ]

    TEMP_UNIT_CHOICES = [
        ('°C', '°C'),
        ('°F', '°F'),
    ]

    # --- Basic info ---
    machine_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Running',
        db_index=True,
    )

    # --- Monitoring ---
    temperature = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    temperature_unit = models.CharField(
        max_length=5,
        choices=TEMP_UNIT_CHOICES,
        default='°C',
    )
    pressure = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    rpm = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
    )

    # --- Maintenance ---
    maintenance_date = models.DateField()
    downtime_reason = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    # --- Analytics ---
    efficiency = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('90.00'),
        validators=[
            MinValueValidator(Decimal('0.00')),
            MaxValueValidator(Decimal('100.00')),
        ],
        help_text="Efficiency percentage (0-100)",
    )

    # --- Timestamp ---
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Machine'
        verbose_name_plural = 'Machines'
        indexes = [
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.machine_id} — {self.status}"