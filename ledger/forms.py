from django import forms
from .models import Client, LedgerEntry


class ClientForm(forms.ModelForm):
    """Form to add a new client — no pre-filled zeros."""

    # Override numeric fields with optional=True and no initial
    opening_balance = forms.DecimalField(
        required=False,
        initial=None,  # 🔥 No 0.00 pre-fill
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opening balance (₹)',
            'step': '0.01',
            'autocomplete': 'off',
        }),
        min_value=0,
    )

    class Meta:
        model = Client
        fields = ['name', 'phone', 'address', 'opening_balance', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Client name (e.g. RAJU)',
                'autofocus': True,
                'autocomplete': 'off',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-digit phone number',
                'autocomplete': 'off',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Full address (optional)',
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }

    def clean_name(self):
        name = (self.cleaned_data.get('name') or '').strip()
        if not name:
            raise forms.ValidationError("Client name is required.")
        return name

    def clean_phone(self):
        phone = (self.cleaned_data.get('phone') or '').strip()
        if phone and len(phone.replace(' ', '').replace('-', '')) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits.")
        return phone

    def clean_opening_balance(self):
        balance = self.cleaned_data.get('opening_balance')
        if balance is None:
            return 0
        return balance


class LedgerEntryForm(forms.ModelForm):
    """Form for SALE or PAYMENT — no pre-filled zeros."""

    # 🔥 Override numeric fields to blank by default
    quantity = forms.DecimalField(
        required=False,
        initial=None,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quantity (kg)',
            'step': '0.01',
            'min': 0,
            'id': 'id_quantity',
            'autocomplete': 'off',
        }),
        min_value=0,
    )

    rate = forms.DecimalField(
        required=False,
        initial=None,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rate per unit (₹)',
            'step': '0.01',
            'min': 0,
            'id': 'id_rate',
            'autocomplete': 'off',
        }),
        min_value=0,
    )

    payment_amount = forms.DecimalField(
        required=False,
        initial=None,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Payment amount (₹)',
            'step': '0.01',
            'min': 0,
            'id': 'id_payment_amount',
            'autocomplete': 'off',
        }),
        min_value=0,
    )

    class Meta:
        model = LedgerEntry
        fields = [
            'entry_type', 'date', 'bill_no', 'description',
            'quantity', 'rate',
            'payment_date', 'payment_amount', 'pay_type',
        ]
        widgets = {
            'entry_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_entry_type',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'bill_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Invoice / Bill number',
                'autocomplete': 'off',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. DANA 3000 kg',
                'autocomplete': 'off',
            }),
            'payment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_payment_date',
            }),
            'pay_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_pay_type',
            }),
        }

    def clean(self):
        cleaned = super().clean()
        entry_type = cleaned.get('entry_type')

        if entry_type == 'SALE':
            qty = cleaned.get('quantity')
            rate = cleaned.get('rate')
            if not qty or qty <= 0:
                raise forms.ValidationError("Quantity must be greater than 0 for a SALE.")
            if not rate or rate <= 0:
                raise forms.ValidationError("Rate must be greater than 0 for a SALE.")

        elif entry_type == 'PAYMENT':
            amount = cleaned.get('payment_amount')
            if not amount or amount <= 0:
                raise forms.ValidationError("Payment amount must be greater than 0.")

        return cleaned