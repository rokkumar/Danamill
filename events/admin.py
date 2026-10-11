from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Event, EventItem


class EventItemInline(admin.TabularInline):
    model = EventItem
    extra = 0
    fields = ['item_name', 'total_cost', 'paid_amount', 'notes']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'total_collection', 'is_active', 'view_link']
    list_filter = ['is_active', 'start_date']
    search_fields = ['name', 'description']
    inlines = [EventItemInline]
    readonly_fields = ['created_at', 'updated_at']

    def view_link(self, obj):
        url = reverse('events:event_detail', args=[obj.id])
        return format_html(
            '<a href="{}" target="_blank" '
            'style="background:#7c3aed;color:white;padding:5px 12px;'
            'border-radius:6px;text-decoration:none;font-weight:600;'
            'font-size:12px;">View Statement</a>',
            url,
        )
    view_link.short_description = 'Statement'


@admin.register(EventItem)
class EventItemAdmin(admin.ModelAdmin):
    list_display = ['event', 'item_name', 'total_cost', 'paid_amount', 'pending_display']
    list_filter = ['event']
    search_fields = ['item_name', 'notes']

    def pending_display(self, obj):
        return f"₹{obj.pending_amount():,.2f}"
    pending_display.short_description = 'Pending'