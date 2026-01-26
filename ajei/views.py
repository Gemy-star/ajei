from django.shortcuts import render, redirect
from django.utils import translation
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST
from constance import config
from .models import ContactSubmission


def get_client_ip(request):
    """Get the client's IP address from the request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def ajei_landing_page(request):
    """
    Main landing page view for Ajei project
    """
    # Handle language switching
    lang = request.GET.get('lang')
    if lang in ['en', 'ar']:
        translation.activate(lang)
        request.session['django_language'] = lang

    context = {
        'config': config,
    }
    return render(request, 'landing_page/ajei_landing.html', context)


def ajei_page(request):
    """
    Alternative Ajei page view
    """
    # Handle language switching
    lang = request.GET.get('lang')
    if lang in ['en', 'ar']:
        translation.activate(lang)
        request.session['django_language'] = lang

    context = {
        'config': config,
    }
    return render(request, 'landing_page/ajei.html', context)


@require_POST
def ajei_contact_submit(request):
    """
    Handle contact form submissions
    """
    try:
        # Check if contact form is enabled
        if not config.ENABLE_CONTACT_FORM:
            messages.warning(request, 'نعتذر، نموذج الاتصال غير متاح حالياً.')
            return redirect('landing_page')

        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        investment_type = request.POST.get('investment_type', '').strip()

        # Basic validation
        if not all([name, email, phone]):
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')
            return redirect('landing_page')

        # Create contact submission
        contact = ContactSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
            investment_type=investment_type if investment_type else None,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            referrer=request.META.get('HTTP_REFERER', '')[:500],
        )

        # Success message
        messages.success(request, 'شكراً لتواصلك معنا! سنقوم بالرد عليك قريباً.')

    except Exception as e:
        messages.error(request, 'حدث خطأ في إرسال الرسالة. يرجى المحاولة مرة أخرى.')
        print(f"Error saving contact submission: {e}")
