from django import forms
from .models import Production


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = [
            'batch', 'machine', 'material', 'shift',
            'output', 'scrap', 'status',
            'production_date', 'notes',
        ]
        widgets = {
            'batch': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. BATCH-2026-001',
            }),
            'machine': forms.Select(attrs={'class': 'form-control'}),
            'material': forms.Select(attrs={'class': 'form-control'}),
            'shift': forms.Select(attrs={'class': 'form-control'}),
            'output': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Output in Kg',
                'min': 1,
            }),
            'scrap': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Scrap in Kg',
                'min': 0,
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'production_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Any additional notes...',
            }),
        }

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def clean_output(self):
        output = self.cleaned_data.get('output')
        if output is None or output <= 0:
            raise forms.ValidationError(
                "Output must be greater than 0."
            )
        return output

    def clean_scrap(self):
        scrap = self.cleaned_data.get('scrap')
        if scrap is None:
            scrap = 0
        if scrap < 0:
            raise forms.ValidationError(
                "Scrap cannot be negative."
            )
        return scrap

    def clean_batch(self):
        batch = self.cleaned_data.get('batch', '').strip()
        if not batch:
            raise forms.ValidationError(
                "Batch ID is required."
            )
        return batch