from django.db import models

class Order(models.Model):
    product = models.CharField(max_length=100)          # free text, no choices
    quantity = models.PositiveIntegerField(default=1)
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer_name} - {self.product}"
