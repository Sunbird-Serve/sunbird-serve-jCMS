# from django.http import HttpResponse
from cms.models import *
# from django.urls import reverse
from django.http import HttpResponseForbidden

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.path.startswith('/api/'):
            api_key = request.META.get('HTTP_APIKEY')
            if not self.is_valid_api_key(api_key):
                return HttpResponseForbidden("Invalid API key")
        
        # Get the response from the next middleware or the view
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def is_valid_api_key(self, api_key):
        try:
            keyval = APIKey.objects.get(key=api_key)
            return api_key == keyval.key
        except APIKey.DoesNotExist:
            return False