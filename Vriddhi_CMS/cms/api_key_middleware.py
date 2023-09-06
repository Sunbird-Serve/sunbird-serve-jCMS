from django.http import HttpResponse
from cms.models import *
from django.core.urlresolvers import reverse

class APIKeyMiddleware(object):

    def process_request(self, request):
        admin_url = reverse('admin:index')  # Adjust the name if necessary
        if request.path.startswith(admin_url):
            # Exclude processing for admin URLs
            return None
        else:
            api_key = request.META.get('HTTP_APIKEY')
            if not self.is_valid_api_key(api_key):
                return HttpResponseForbidden("Invalid API key")
            return None

    def is_valid_api_key(self, api_key):
        print(api_key)
        keyval = APIKey.objects.get(key=api_key)
        print("databaseKey:",keyval.key)
        return api_key == keyval.key  # Replace with your actual key