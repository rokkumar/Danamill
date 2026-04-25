from django.contrib import admin
from django.utils.html import format_html
from .models import Enquiry, EnquiryLog

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'product', 'status', 'created_at', 'admin_actions']
    list_filter = ['status', 'product', 'created_at', 'is_read']
    search_fields = ['name', 'email', 'phone', 'message']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Enquiry Details', {
            'fields': ('product', 'message', 'quantity', 'preferred_contact_time')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'is_read')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_read', 'mark_as_contacted', 'mark_as_completed']
    
    def admin_actions(self, obj):
        return format_html(
            '<a class="button" href="/admin/Enquiry/enquiry/{}/change/">View</a>',
            obj.id
        )
    admin_actions.short_description = 'Actions'
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected enquiries as read"
    
    def mark_as_contacted(self, request, queryset):
        queryset.update(status='contacted')
    mark_as_contacted.short_description = "Mark selected as contacted"
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected as completed"

@admin.register(EnquiryLog)
class EnquiryLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'enquiry', 'email_type', 'sent_to', 'status', 'created_at']
    list_filter = ['status', 'email_type', 'created_at']
    search_fields = ['sent_to', 'error_message']
    readonly_fields = ['created_at']