"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ajei import views as ajei_views

urlpatterns = [
    path("", ajei_views.ajei_landing_page, name="landing_page"),
    path("ajei/", ajei_views.ajei_page, name="ajei_page"),
    path("contact/submit/", ajei_views.ajei_contact_submit, name="ajei_contact_submit"),
    path("dashboard/", ajei_views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/contacts/", ajei_views.contact_list, name="contact_list"),
    path(
        "dashboard/contact/<int:contact_id>/",
        ajei_views.contact_detail,
        name="contact_detail",
    ),
    path(
        "dashboard/contact/<int:contact_id>/update/",
        ajei_views.update_contact_status,
        name="update_contact_status",
    ),
    path(
        "dashboard/translations/",
        ajei_views.translations_page,
        name="translations_page",
    ),
    # Redirect old rosetta pick URLs
    path(
        "rosetta/pick/<str:lang_code>/",
        ajei_views.rosetta_pick_redirect,
        name="rosetta_pick_redirect",
    ),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("rosetta/", include("rosetta.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
