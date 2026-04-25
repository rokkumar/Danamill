from django.db import models
from django.utils import timezone

class Enquiry(models.Model):
    """
    Model to store customer enquiries from the quick enquiry form
    """
    
    PRODUCT_CHOICES = [
        ('HDPE Granules', 'HDPE Granules'),
        ('LDPE Granules', 'LDPE Granules'),
        ('PP Granules', 'PP Granules'),
        ('Recycled Granules', 'Recycled Granules'),
        ('Other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('contacted', 'Contacted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Personal Information
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=15, verbose_name="Phone Number")
    
    # Enquiry Details
    product = models.CharField(max_length=50, choices=PRODUCT_CHOICES, verbose_name="Product")
    message = models.TextField(verbose_name="Message / Quantity Required", blank=True)
    
    # Additional Information
    quantity = models.CharField(max_length=100, blank=True, verbose_name="Quantity Required")
    preferred_contact_time = models.CharField(max_length=100, blank=True, verbose_name="Preferred Contact Time")
    
    # Status and Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    is_read = models.BooleanField(default=False, verbose_name="Mark as Read")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        db_table = 'enquiries'
        verbose_name = 'Enquiry'
        verbose_name_plural = 'Enquiries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.product} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def save(self, *args, **kwargs):
        # Auto-extract quantity from message if not provided separately
        if not self.quantity and self.message:
            import re
            # Try to extract quantity (numbers followed by kg, ton, etc.)
            quantity_pattern = r'(\d+(?:\.\d+)?)\s*(?:kg|KG|Kg|ton|TON|Ton|MT|mt|quintal)'
            match = re.search(quantity_pattern, self.message)
            if match:
                self.quantity = match.group(0)
        super().save(*args, **kwargs)

class EnquiryLog(models.Model):
    """
    Model to track email sending status for enquiries
    """
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name='logs')
    email_type = models.CharField(max_length=50)  # admin_notification, customer_acknowledgment
    sent_to = models.EmailField()
    status = models.CharField(max_length=20)  # success, failed
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'enquiry_logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email_type} to {self.sent_to} - {self.status}"