from django.shortcuts import render, redirect
from django.utils import translation
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db.models.functions import TruncDate, TruncHour
from django.utils import timezone
from datetime import timedelta
from constance import config
from .models import ContactSubmission, PageView


def get_client_ip(request):
    """Get the client's IP address from the request"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def ajei_landing_page(request):
    """
    Main landing page view for Ajei project
    """
    # Handle language switching
    lang = request.GET.get("lang")
    if lang in ["en", "ar"]:
        translation.activate(lang)
        request.session["django_language"] = lang
        request.session.modified = True
        # Create response and set language cookie
        response = redirect(request.path)
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
        return response

    # Get current language
    current_lang = translation.get_language()

    context = {
        "config": config,
        "current_language": current_lang,
    }
    return render(request, "landing_page/ajei_landing.html", context)


def ajei_page(request):
    """
    Alternative Ajei page view
    """
    # Handle language switching
    lang = request.GET.get("lang")
    if lang in ["en", "ar"]:
        translation.activate(lang)
        request.session["django_language"] = lang
        request.session.modified = True
        # Create response and set language cookie
        response = redirect(request.path)
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
        return response

    # Get current language
    current_lang = translation.get_language()

    context = {
        "config": config,
        "current_language": current_lang,
    }
    return render(request, "landing_page/ajei.html", context)


@require_POST
def ajei_contact_submit(request):
    """
    Handle contact form submissions
    """
    try:
        # Check if contact form is enabled
        if not config.ENABLE_CONTACT_FORM:
            messages.warning(request, "نعتذر، نموذج الاتصال غير متاح حالياً.")
            return redirect("landing_page")

        # Get form data
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()
        investment_type = request.POST.get("investment_type", "").strip()

        # Basic validation
        if not all([name, email, phone]):
            messages.error(request, "يرجى ملء جميع الحقول المطلوبة.")
            return redirect("landing_page")

        # Create contact submission
        contact = ContactSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
            investment_type=investment_type if investment_type else None,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
            referrer=request.META.get("HTTP_REFERER", "")[:500],
        )

        # Success message
        messages.success(request, "شكراً لتواصلك معنا! سنقوم بالرد عليك قريباً.")
        return redirect("landing_page")

    except Exception as e:
        messages.error(request, "حدث خطأ في إرسال الرسالة. يرجى المحاولة مرة أخرى.")
        print(f"Error saving contact submission: {e}")
        return redirect("landing_page")


@login_required
def admin_dashboard(request):
    """
    Admin dashboard with statistics and management tools
    """
    # Date ranges
    now = timezone.now()
    today = now.date()
    last_7_days = now - timedelta(days=7)
    last_30_days = now - timedelta(days=30)

    # Contact Submissions Stats
    total_contacts = ContactSubmission.objects.count()
    new_contacts = ContactSubmission.objects.filter(status="new").count()
    contacts_today = ContactSubmission.objects.filter(created_at__date=today).count()
    contacts_this_week = ContactSubmission.objects.filter(
        created_at__gte=last_7_days
    ).count()
    contacts_this_month = ContactSubmission.objects.filter(
        created_at__gte=last_30_days
    ).count()

    # Recent contacts
    recent_contacts = ContactSubmission.objects.select_related().order_by(
        "-created_at"
    )[:10]

    # Contact by status
    contacts_by_status = (
        ContactSubmission.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Contact by investment type
    contacts_by_type = (
        ContactSubmission.objects.exclude(
            Q(investment_type__isnull=True) | Q(investment_type="")
        )
        .values("investment_type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Page Views Stats
    total_views = PageView.objects.count()
    views_today = PageView.objects.filter(viewed_at__date=today).count()
    views_this_week = PageView.objects.filter(viewed_at__gte=last_7_days).count()
    views_this_month = PageView.objects.filter(viewed_at__gte=last_30_days).count()

    # Unique visitors (by IP)
    unique_visitors_today = (
        PageView.objects.filter(viewed_at__date=today)
        .values("ip_address")
        .distinct()
        .count()
    )

    unique_visitors_week = (
        PageView.objects.filter(viewed_at__gte=last_7_days)
        .values("ip_address")
        .distinct()
        .count()
    )

    # Most viewed pages
    popular_pages = (
        PageView.objects.values("page_path")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    # Views by day (last 7 days)
    views_by_day = (
        PageView.objects.filter(viewed_at__gte=last_7_days)
        .annotate(day=TruncDate("viewed_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    # Views by hour (last 24 hours)
    last_24_hours = now - timedelta(hours=24)
    views_by_hour = (
        PageView.objects.filter(viewed_at__gte=last_24_hours)
        .annotate(hour=TruncHour("viewed_at"))
        .values("hour")
        .annotate(count=Count("id"))
        .order_by("hour")
    )

    # Language distribution
    language_stats = (
        PageView.objects.exclude(Q(language="") | Q(language__isnull=True))
        .values("language")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    context = {
        "total_contacts": total_contacts,
        "new_contacts": new_contacts,
        "contacts_today": contacts_today,
        "contacts_this_week": contacts_this_week,
        "contacts_this_month": contacts_this_month,
        "recent_contacts": recent_contacts,
        "contacts_by_status": contacts_by_status,
        "contacts_by_type": contacts_by_type,
        "total_views": total_views,
        "views_today": views_today,
        "views_this_week": views_this_week,
        "views_this_month": views_this_month,
        "unique_visitors_today": unique_visitors_today,
        "unique_visitors_week": unique_visitors_week,
        "popular_pages": popular_pages,
        "views_by_day": views_by_day,
        "views_by_hour": views_by_hour,
        "language_stats": language_stats,
    }

    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
def update_contact_status(request, contact_id):
    """
    Update contact submission status
    """
    if request.method == "POST":
        try:
            contact = ContactSubmission.objects.get(id=contact_id)
            new_status = request.POST.get("status")
            notes = request.POST.get("notes", "")

            if new_status in dict(ContactSubmission.STATUS_CHOICES):
                contact.status = new_status
                if notes:
                    contact.notes = notes
                contact.save()
                messages.success(request, "تم تحديث حالة الطلب بنجاح")
            else:
                messages.error(request, "حالة غير صالحة")
        except ContactSubmission.DoesNotExist:
            messages.error(request, "الطلب غير موجود")
        except Exception as e:
            messages.error(request, f"حدث خطأ: {str(e)}")

    return redirect("admin_dashboard")


@login_required
def contact_detail(request, contact_id):
    """
    View detailed information about a contact submission
    """
    try:
        contact = ContactSubmission.objects.get(id=contact_id)
    except ContactSubmission.DoesNotExist:
        messages.error(request, "الطلب غير موجود")
        return redirect("admin_dashboard")

    context = {
        "contact": contact,
    }
    return render(request, "dashboard/contact_detail.html", context)


@login_required
def contact_list(request):
    """
    List all contact submissions with filtering
    """
    status_filter = request.GET.get("status", "")
    search = request.GET.get("search", "")

    contacts = ContactSubmission.objects.all()

    if status_filter:
        contacts = contacts.filter(status=status_filter)

    if search:
        contacts = contacts.filter(
            Q(name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
        )

    contacts = contacts.order_by("-created_at")

    context = {
        "contacts": contacts,
        "status_choices": ContactSubmission.STATUS_CHOICES,
        "current_status": status_filter,
        "search_query": search,
    }
    return render(request, "dashboard/contact_list.html", context)


@login_required
def translations_page(request):
    """
    Custom translations management page
    """
    import os
    from django.conf import settings

    # Find the translation files
    locale_path = os.path.join(settings.BASE_DIR, "locale")

    # Build proper Rosetta URLs for each language
    # Rosetta uses file IDs, so we'll direct to main page for selection
    context = {
        "languages": [
            {
                "code": "ar",
                "name": "العربية",
                "flag": "🇸🇦",
                "description": "تحرير الترجمة العربية للموقع",
                "file_path": os.path.join(
                    locale_path, "ar", "LC_MESSAGES", "django.po"
                ),
            },
            {
                "code": "en",
                "name": "English",
                "flag": "🇬🇧",
                "description": "Edit English translations",
                "file_path": os.path.join(
                    locale_path, "en", "LC_MESSAGES", "django.po"
                ),
            },
        ],
    }
    return render(request, "dashboard/translations.html", context)


def rosetta_pick_redirect(request, lang_code):
    """
    Redirect old rosetta pick URLs to the main rosetta page
    """
    from django.shortcuts import redirect
    from django.contrib import messages

    messages.info(request, f"يرجى اختيار ملف الترجمة ({lang_code}) من قائمة Rosetta.")
    return redirect("/rosetta/")
