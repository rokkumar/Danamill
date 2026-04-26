
# forms.py (FULL FINAL CORRECT VERSION)

from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'product',
            'quantity',
            'customer_name',
            'email',
            'phone',
            'address',
            'message'
        ]

        widgets = {
            'product': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Product Name'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Enter Quantity (kg/lots)'
            }),

            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Full Name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email Address'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter Delivery Address'
            }),

            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write Additional Message'
            }),
        }

