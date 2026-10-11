from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Client, LedgerEntry


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'phone', 'opening_balance',
        'outstanding_display', 'view_ledger_link', 'is_active',
    ]
    list_filter = ['is_active']
    search_fields = ['name', 'phone']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']

    def outstanding_display(self, obj):
        return f"₹{obj.outstanding():,.2f}"
    outstanding_display.short_description = 'Outstanding'

    def view_ledger_link(self, obj):
        url = reverse('ledger:client_ledger', args=[obj.id])
        return format_html(
            '<a href="{}" target="_blank" '
            'style="background:#4f46e5;color:#fff;padding:5px 12px;'
            'border-radius:6px;text-decoration:none;font-weight:600;'
            'font-size:12px;">View Ledger</a>',
            url,
        )
    view_ledger_link.short_description = 'Ledger'


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = [
        'client', 'entry_type', 'date', 'bill_no', 'description',
        'quantity', 'rate', 'amount', 'payment_date',
        'payment_amount', 'pay_type',
    ]
    list_filter = ['entry_type', 'pay_type', 'date']
    search_fields = ['client__name', 'bill_no', 'description']
    date_hierarchy = 'date'
    list_per_page = 50
    autocomplete_fields = ['client']

    fieldsets = (
        ('Client', {
            'fields': ('client', 'entry_type'),
        }),
        ('Sale Details (only for SALE rows)', {
            'fields': ('date', 'bill_no', 'description', 'quantity', 'rate'),
            'classes': ('wide',),
            'description': 'Fill these fields only for SALE entries.',
        }),
        ('Payment Details (only for PAYMENT rows)', {
            'fields': ('payment_date', 'payment_amount', 'pay_type'),
            'classes': ('wide',),
            'description': 'Fill these fields only for PAYMENT entries.',
        }),
    )