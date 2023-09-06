from django.core.management.base import BaseCommand
from cms.models import APIKey
from django.contrib.auth.models import User
from django.core.cache import cache  # Import the cache module

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Clear the cache before generating API keys
        cache.clear()

        for user in User.objects.all():
            APIKey.objects.create(user=user)
        self.stdout.write(self.style.SUCCESS('API keys generated successfully.'))
