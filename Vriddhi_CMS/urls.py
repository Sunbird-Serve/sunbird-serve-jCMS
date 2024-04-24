from django.urls import include, path, re_path
from django.contrib import admin
from django.views.static import serve as static_serve
from django.conf import settings
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cms.urls')),  # Assuming 'cms.urls' is a module with further URL patterns

    # Static files in development (Django does not serve static files in production without additional configuration)
    re_path(r'^static/admin/(?P<path>.*)$', static_serve, {'document_root': settings.ADMIN_MEDIA_PREFIX}),
    re_path(r'^static/(?P<path>.*)$', static_serve, {'document_root': settings.STATIC_ROOT}),
]