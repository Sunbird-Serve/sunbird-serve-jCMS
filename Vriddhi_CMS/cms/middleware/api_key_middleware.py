from cms.models import APIKey

class APIKeyMiddleware(object):
    def process_request(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')

        try:
            api_key_object = APIKey.objects.get(key=api_key)
        except APIKey.DoesNotExist:
            return JsonResponse({'error': 'Invalid API key'}, status=401)