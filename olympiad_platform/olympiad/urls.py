"""olympiad URL Configuration"""

from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.olympiads.urls')),
    path('', include('apps.students.urls')),
    path('', include('apps.courses.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "olympiad.views.page_not_found"

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
