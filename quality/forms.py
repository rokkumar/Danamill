from django import forms
from .models import Quality


class QualityForm(forms.ModelForm):

    class Meta:
        model = Quality
        fields = [
            'batch_id',
            'mfi',
            'density',
            'moisture',
            'qc_result',
            'test_date',
        ]
        widgets = {
            'batch_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. BATCH-2026-001',
            }),
            'mfi': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'MFI',
                'step': '0.01',
                'min': 0,
            }),
            'density': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Density (g/cm³)',
                'step': '0.001',
                'min': 0,
            }),
            'moisture': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Moisture (%)',
                'step': '0.01',
                'min': 0,
            }),
            'qc_result': forms.Select(attrs={
                'class': 'form-control',
            }),
            'test_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def clean_batch_id(self):
        batch_id = (self.cleaned_data.get('batch_id') or '').strip()
        if not batch_id:
            raise forms.ValidationError("Batch ID is required.")
        return batch_id

    def clean_mfi(self):
        mfi = self.cleaned_data.get('mfi')
        if mfi is not None and mfi < 0:
            raise forms.ValidationError("MFI cannot be negative.")
        return mfi

    def clean_density(self):
        density = self.cleaned_data.get('density')
        if density is not None and density < 0:
            raise forms.ValidationError("Density cannot be negative.")
        return density

    def clean_moisture(self):
        moisture = self.cleaned_data.get('moisture')
        if moisture is not None and moisture < 0:
            raise forms.ValidationError("Moisture cannot be negative.")
        return moisture