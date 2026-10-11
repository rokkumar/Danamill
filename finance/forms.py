from django import forms
from .models import Finance


class _BaseFinanceForm(forms.ModelForm):
    """Shared widget setup for both Income and Expense forms."""

    class Meta:
        model = Finance
        fields = ['title', 'category', 'amount', 'description', 'date', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title',
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount in ₹',
                'min': 0,
                'step': '0.01',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Optional description',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = (self.cleaned_data.get('title') or '').strip()
        if not title:
            raise forms.ValidationError("Title is required.")
        return title

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        return amount


class IncomeForm(_BaseFinanceForm):
    """Form for adding income records."""
    pass


class ExpenseForm(_BaseFinanceForm):
    """Form for adding expense records."""
    pass