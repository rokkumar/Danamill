from django import forms
from .models import Dispatch


class DispatchForm(forms.ModelForm):

    class Meta:
        model = Dispatch
        fields = [
            'dispatch_id',
            'customer_name',
            'product_name',
            'quantity',
            'vehicle_number',
            'driver_name',
            'dispatch_status',
            'dispatch_date',
        ]
        widgets = {
            'dispatch_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. DSP-2026-001',
            }),
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer name',
            }),
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. HDPE Granules',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Quantity in Kg',
            }),
            'vehicle_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. TS 09 AB 1234',
            }),
            'driver_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Driver name',
            }),
            'dispatch_status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'dispatch_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def clean_dispatch_id(self):
        dispatch_id = (self.cleaned_data.get('dispatch_id') or '').strip()
        if not dispatch_id:
            raise forms.ValidationError("Dispatch ID is required.")
        return dispatch_id

    def clean_customer_name(self):
        name = (self.cleaned_data.get('customer_name') or '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Customer name must be at least 2 characters.")
        return name

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty is None or qty <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return qty