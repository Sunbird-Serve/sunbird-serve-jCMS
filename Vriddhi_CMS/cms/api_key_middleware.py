from django.http import HttpResponse
from cms.models import *
from django.core.urlresolvers import reverse

class APIKeyMiddleware(object):

    def process_request(self, request):
        if request.path.startswith('/api/'):
            api_key = request.META.get('HTTP_APIKEY')
            if not self.is_valid_api_key(api_key):
                return HttpResponseForbidden("Invalid API key")
            return None

    def is_valid_api_key(self, api_key):
        keyval = APIKey.objects.get(key=api_key)
        return api_key == keyval.key 