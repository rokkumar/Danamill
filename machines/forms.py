from django import forms
from .models import Machine


class MachineForm(forms.ModelForm):

    class Meta:
        model = Machine
        fields = [
            'machine_id',
            'status',
            'temperature',
            'temperature_unit',
            'pressure',
            'rpm',
            'maintenance_date',
            'downtime_reason',
        ]
        widgets = {
            'machine_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. M-001',
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'temperature': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Temperature',
                'step': '0.01',
                'min': 0,
            }),
            'temperature_unit': forms.Select(attrs={'class': 'form-control'}),
            'pressure': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pressure',
                'step': '0.01',
                'min': 0,
            }),
            'rpm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'RPM',
                'min': 0,
            }),
            'maintenance_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'downtime_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Reason for downtime (optional)',
                'rows': 3,
            }),
        }

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def clean_machine_id(self):
        machine_id = (self.cleaned_data.get('machine_id') or '').strip()
        if not machine_id:
            raise forms.ValidationError("Machine ID is required.")
        return machine_id

    def clean_temperature(self):
        temp = self.cleaned_data.get('temperature')
        if temp is not None and temp < 0:
            raise forms.ValidationError("Temperature cannot be negative.")
        return temp

    def clean_pressure(self):
        pressure = self.cleaned_data.get('pressure')
        if pressure is not None and pressure < 0:
            raise forms.ValidationError("Pressure cannot be negative.")
        return pressure

    def clean_rpm(self):
        rpm = self.cleaned_data.get('rpm')
        if rpm is not None and rpm < 0:
            raise forms.ValidationError("RPM cannot be negative.")
        return rpm