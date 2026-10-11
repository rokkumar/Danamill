from django import forms
from .models import Inventory


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['material', 'quantity', 'supplier', 'date', 'scrap']
        widgets = {
            'material': forms.Select(attrs={
                'class': 'form-control',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 500',
                'min': 0,
            }),
            'supplier': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Supplier name',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'scrap': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 10',
                'min': 0,
            }),
        }

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty is not None and qty < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return qty

    def clean_scrap(self):
        scrap = self.cleaned_data.get('scrap')
        if scrap is not None and scrap < 0:
            raise forms.ValidationError("Scrap cannot be negative.")
        return scrap

    def clean(self):
        cleaned = super().clean()
        qty = cleaned.get('quantity')
        scrap = cleaned.get('scrap')
        if qty is not None and scrap is not None and scrap > qty:
            raise forms.ValidationError(
                "Scrap cannot be greater than the total quantity."
            )
        return cleaned