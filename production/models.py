from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class Production(models.Model):

    MACHINE_CHOICES = [
        ('Machine 1', 'Machine 1'),
        ('Machine 2', 'Machine 2'),
        ('Machine 3', 'Machine 3'),
    ]

    MATERIAL_CHOICES = [
        ('HDPE', 'HDPE'),
        ('LDPE', 'LDPE'),
        ('PP', 'PP'),
    ]

    SHIFT_CHOICES = [
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
        ('Night', 'Night'),
    ]

    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Running', 'Running'),
        ('Pending', 'Pending'),
    ]

    # --- Basic info ---
    batch = models.CharField(max_length=100, db_index=True)
    machine = models.CharField(max_length=50, choices=MACHINE_CHOICES)
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
    shift = models.CharField(
        max_length=20, choices=SHIFT_CHOICES, default='Morning'
    )

    # --- Production figures ---
    output = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Output in Kg"
    )
    scrap = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Scrap in Kg"
    )
    efficiency = models.FloatField(
        default=0,
        help_text="Auto-calculated (output / (output + scrap) * 100)"
    )

    # --- Status & notes ---
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Completed'
    )
    notes = models.TextField(blank=True, null=True)
    production_date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-production_date', '-id']
        verbose_name = "Production Entry"
        verbose_name_plural = "Production Entries"
        indexes = [
            models.Index(fields=['batch']),
            models.Index(fields=['machine']),
            models.Index(fields=['shift']),
            models.Index(fields=['production_date']),
        ]

    def __str__(self):
        return f"{self.batch} — {self.machine}"

    def save(self, *args, **kwargs):
        total = (self.output or 0) + (self.scrap or 0)
        if total > 0:
            self.efficiency = round((self.output / total) * 100, 2)
        else:
            self.efficiency = 0
        super().save(*args, **kwargs)

    @property
    def total_input(self):
        return (self.output or 0) + (self.scrap or 0)