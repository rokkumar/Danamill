from django import forms
from .models import Event, EventItem


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'total_collection', 'start_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Ganesh Navratri 2026',
                'autofocus': True,
                'autocomplete': 'off',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Comprehensive Bill Summary',
                'autocomplete': 'off',
            }),
            'total_collection': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Total funds collected (₹)',
                'step': '0.01',
                'min': 0,
                'autocomplete': 'off',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }

    # Force blank default
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['total_collection'].initial = None

    def clean_name(self):
        name = (self.cleaned_data.get('name') or '').strip()
        if not name:
            raise forms.ValidationError("Event name is required.")
        return name


class EventItemForm(forms.ModelForm):
    class Meta:
        model = EventItem
        fields = ['item_name', 'total_cost', 'paid_amount', 'notes']
        widgets = {
            'item_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Decoration',
                'autofocus': True,
                'autocomplete': 'off',
            }),
            'total_cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Total cost (₹)',
                'step': '0.01',
                'min': 0,
                'autocomplete': 'off',
            }),
            'paid_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Paid amount (₹)',
                'step': '0.01',
                'min': 0,
                'autocomplete': 'off',
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional notes',
                'autocomplete': 'off',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['paid_amount'].initial = None

    def clean(self):
        cleaned = super().clean()
        cost = cleaned.get('total_cost')
        paid = cleaned.get('paid_amount')

        if cost is None or cost < 0:
            raise forms.ValidationError("Total cost must be a positive number.")

        if paid is None:
            paid = 0
            cleaned['paid_amount'] = 0

        if paid < 0:
            raise forms.ValidationError("Paid amount cannot be negative.")

        if paid > cost:
            raise forms.ValidationError("Paid amount cannot exceed total cost.")

        return cleaned