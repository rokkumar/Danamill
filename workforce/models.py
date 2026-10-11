from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Employee(models.Model):
    SHIFT_CHOICES = [
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
        ('Night', 'Night'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    shift = models.CharField(
        max_length=20, choices=SHIFT_CHOICES, default='Morning'
    )
    machine = models.CharField(max_length=50, blank=True)
    attendance = models.BooleanField(default=False)
    productivity = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        help_text="Productivity percentage (0–100)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.name} — {self.role or 'Employee'}"