from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Inventory(models.Model):
    MATERIAL_CHOICES = [
        ('HDPE', 'HDPE'),
        ('LDPE', 'LDPE'),
        ('PP', 'PP'),
    ]

    material = models.CharField(max_length=10, choices=MATERIAL_CHOICES)
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Quantity in Kg (must be 0 or more)"
    )
    supplier = models.CharField(max_length=100)
    date = models.DateField()
    scrap = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Scrap in Kg (must be 0 or more)"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-id']
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory"

    def __str__(self):
        return f"{self.material} — {self.quantity} Kg"

    @property
    def net_quantity(self):
        """Actual usable quantity after scrap."""
        return max(0, self.quantity - self.scrap)