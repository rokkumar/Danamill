from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'role', 'shift', 'machine', 'productivity']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Employee name',
            }),
            'role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Operator',
            }),
            'shift': forms.Select(attrs={
                'class': 'form-control',
            }),
            'machine': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Machine ID (optional)',
            }),
            'productivity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 85',
                'min': 0,
                'max': 100,
            }),
        }

    def clean_productivity(self):
        p = self.cleaned_data.get('productivity')
        if p is not None and (p < 0 or p > 100):
            raise forms.ValidationError(
                "Productivity must be between 0 and 100."
            )
        return p