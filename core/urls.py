import statistics
from django.contrib import admin
from django.urls import include, path

from core import settings

admin.site.site_header = 'Mandera File Management System'
admin.site.site_title = 'Office Of The Governor'

urlpatterns = [
    # path('admin/defender/', include('defender.urls')), # defender admin
    path('admin/', admin.site.urls),
    path('', include('fms.urls')),
    path('', include('account.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

