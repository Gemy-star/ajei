from django.utils.deprecation import MiddlewareMixin
from django.utils import translation
from .models import PageView


class PageViewTrackingMiddleware(MiddlewareMixin):
    """
    Middleware to track page views for analytics
    """

    def process_response(self, request, response):
        """
        Track page views after response is generated
        """
        # Only track successful GET requests (200 status)
        if request.method == "GET" and response.status_code == 200:
            # Skip admin, static, media, and dashboard pages
            path = request.path
            skip_paths = [
                "/admin/",
                "/static/",
                "/media/",
                "/dashboard/",
                "/rosetta/",
                "/accounts/",
            ]

            if not any(path.startswith(skip_path) for skip_path in skip_paths):
                try:
                    # Get client IP
                    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
                    if x_forwarded_for:
                        ip_address = x_forwarded_for.split(",")[0].strip()
                    else:
                        ip_address = request.META.get("REMOTE_ADDR")

                    # Get current language
                    current_language = translation.get_language()

                    # Create page view record
                    PageView.objects.create(
                        page_path=path,
                        page_title=self._get_page_title(path),
                        ip_address=ip_address,
                        user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
                        referrer=request.META.get("HTTP_REFERER", "")[:500],
                        session_key=request.session.session_key or "",
                        language=current_language or "ar",
                    )
                except Exception as e:
                    # Silently fail to not disrupt user experience
                    print(f"Error tracking page view: {e}")

        return response

    def _get_page_title(self, path):
        """
        Get a friendly page title based on the path
        """
        titles = {
            "/": "الصفحة الرئيسية",
            "/ajei/": "صفحة أجيء",
        }
        return titles.get(path, path)
