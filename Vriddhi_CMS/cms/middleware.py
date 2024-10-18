# from django.http import HttpResponse
from cms.models import *
# from django.urls import reverse
from django.http import HttpResponseForbidden

class CheckRefererMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_referers = [
            'https://serve-v1.evean.net',  # Main application
            'https://serve-jcms.evean.net',  # CMS itself for internal navigation
        ]
        referer = request.META.get('HTTP_REFERER', '')

        if request.path.startswith('/dashboard') or request.path.startswith('/admin_login'):
            return self.get_response(request)

        # Allow access if the referer is from the main app or the CMS itself
        if not any(referer.startswith(allowed_referer) for allowed_referer in allowed_referers):
            return HttpResponseForbidden("Access denied")

        return self.get_response(request)
