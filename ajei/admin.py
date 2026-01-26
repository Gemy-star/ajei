from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.utils import timezone
from .models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing contact form submissions
    """
    list_display = [
        'name',
        'email',
        'phone',
        'investment_type_display',
        'status_badge',
        'created_at',
        'contacted_status'
    ]

    list_filter = [
        'status',
        'investment_type',
        'created_at',
        'contacted_at',
    ]

    search_fields = [
        'name',
        'email',
        'phone',
        'message',
        'notes',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
        'ip_address',
        'user_agent',
        'referrer',
    ]

    fieldsets = (
        (_('Contact Information'), {
            'fields': ('name', 'email', 'phone')
        }),
        (_('Investment Details'), {
            'fields': ('investment_type', 'message')
        }),
        (_('Status & Follow-up'), {
            'fields': ('status', 'notes', 'contacted_at'),
            'classes': ('wide',)
        }),
        (_('Technical Information'), {
            'fields': ('ip_address', 'user_agent', 'referrer'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = [
        'mark_as_contacted',
        'mark_as_qualified',
        'mark_as_converted',
        'mark_as_closed',
    ]

    list_per_page = 25
    date_hierarchy = 'created_at'

    def investment_type_display(self, obj):
        """Display investment type with icon"""
        if not obj.investment_type:
            return '-'

        icons = {
            'medical': '🏥',
            'commercial': '🏢',
            'pharmacy': '💊',
            'restaurant': '🍽️',
            'other': '📋',
        }
        icon = icons.get(obj.investment_type, '📋')
        return f"{icon} {obj.get_investment_type_display()}"
    investment_type_display.short_description = _('Investment Type')

    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'new': '#17a2b8',  # info blue
            'contacted': '#ffc107',  # warning yellow
            'qualified': '#28a745',  # success green
            'converted': '#007bff',  # primary blue
            'closed': '#6c757d',  # secondary gray
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display().upper()
        )
    status_badge.short_description = _('Status')

    def contacted_status(self, obj):
        """Show if and when the contact was reached"""
        if obj.contacted_at:
            return format_html(
                '<span style="color: green;">✓ {}</span>',
                obj.contacted_at.strftime('%Y-%m-%d %H:%M')
            )
        return format_html('<span style="color: red;">✗ Not contacted</span>')
    contacted_status.short_description = _('Contacted')

    def mark_as_contacted(self, request, queryset):
        """Mark selected submissions as contacted"""
        updated = queryset.update(status='contacted', contacted_at=timezone.now())
        self.message_user(request, _(f'{updated} submission(s) marked as contacted.'))
    mark_as_contacted.short_description = _('Mark as Contacted')

    def mark_as_qualified(self, request, queryset):
        """Mark selected submissions as qualified leads"""
        updated = queryset.update(status='qualified')
        self.message_user(request, _(f'{updated} submission(s) marked as qualified.'))
    mark_as_qualified.short_description = _('Mark as Qualified Lead')

    def mark_as_converted(self, request, queryset):
        """Mark selected submissions as converted"""
        updated = queryset.update(status='converted')
        self.message_user(request, _(f'{updated} submission(s) marked as converted.'))
    mark_as_converted.short_description = _('Mark as Converted')

    def mark_as_closed(self, request, queryset):
        """Mark selected submissions as closed"""
        updated = queryset.update(status='closed')
        self.message_user(request, _(f'{updated} submission(s) marked as closed.'))
    mark_as_closed.short_description = _('Mark as Closed')
