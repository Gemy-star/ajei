from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactSubmission(models.Model):
    """
    Model to store contact form submissions from the Ajei landing page
    """
    INVESTMENT_CHOICES = [
        ('medical', _('Medical Unit')),
        ('commercial', _('Commercial Unit')),
        ('pharmacy', _('Pharmacy')),
        ('restaurant', _('Restaurant/Cafe')),
        ('other', _('Other')),
    ]

    STATUS_CHOICES = [
        ('new', _('New')),
        ('contacted', _('Contacted')),
        ('qualified', _('Qualified Lead')),
        ('converted', _('Converted')),
        ('closed', _('Closed')),
    ]

    # Contact Information
    name = models.CharField(_('Full Name'), max_length=200)
    email = models.EmailField(_('Email Address'))
    phone = models.CharField(_('Phone Number'), max_length=20)

    # Investment Details
    investment_type = models.CharField(
        _('Investment Type'),
        max_length=20,
        choices=INVESTMENT_CHOICES,
        blank=True,
        null=True
    )
    message = models.TextField(_('Message'), blank=True)

    # Tracking Information
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    notes = models.TextField(_('Admin Notes'), blank=True)

    # Metadata
    ip_address = models.GenericIPAddressField(_('IP Address'), null=True, blank=True)
    user_agent = models.TextField(_('User Agent'), blank=True)
    referrer = models.URLField(_('Referrer URL'), blank=True, max_length=500)

    # Timestamps
    created_at = models.DateTimeField(_('Submitted At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Last Updated'), auto_now=True)
    contacted_at = models.DateTimeField(_('Contacted At'), null=True, blank=True)

    class Meta:
        verbose_name = _('Contact Submission')
        verbose_name_plural = _('Contact Submissions')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.name} - {self.email} ({self.get_status_display()})"

    def get_investment_display_text(self):
        """Return investment type display text or 'N/A' if not set"""
        return self.get_investment_type_display() if self.investment_type else _('N/A')
