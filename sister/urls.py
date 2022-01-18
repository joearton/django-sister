from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # internal urls
    path('i18n/', include('django.conf.urls.i18n')),
    path('captcha/', include('captcha.urls')),
    path('administrator/', admin.site.urls),

    # frontend and public urls
    path('', include('aurora.frontend.urls')),
    
]


# Maintenance URL
if settings.BACKEND_SETTINGS['maintenance']:
    from aurora.backend.views import maintenance
    urlpatterns += [
        path(settings.BACKEND_SETTINGS['maintenance_path'], maintenance.MaintenanceView.as_view(), name = 'aurora.maintenance')
    ]


# Media URLS
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]