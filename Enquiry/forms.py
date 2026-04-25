from django import forms
from .models import Enquiry

class QuickEnquiryForm(forms.ModelForm):
    """
    Form for the quick enquiry section
    """
    
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'product', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'form-control',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'form-control',
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone Number',
                'class': 'form-control',
                'required': 'required'
            }),
            'product': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }, choices=[
                ('', 'Select Product'),
                ('HDPE Granules', 'HDPE Granules'),
                ('LDPE Granules', 'LDPE Granules'),
                ('PP Granules', 'PP Granules'),
                ('Recycled Granules', 'Recycled Granules'),
            ]),
            'message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Your Message / Quantity Required',
                'class': 'form-control'
            }),
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Basic phone number validation
        if phone and len(phone) < 10:
            raise forms.ValidationError("Please enter a valid phone number (minimum 10 digits)")
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and '@' not in email:
            raise forms.ValidationError("Please enter a valid email address")
        return email