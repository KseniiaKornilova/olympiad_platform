"""olympiad URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import include, path
from django.views.decorators.cache import never_cache

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="api_olympiad_platform",
      default_version='v1',
      description="",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ksyu_kornilova@mail.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.olympiads.urls')),
    path('', include('apps.students.urls')),
    path('', include('apps.courses.urls')),
    path('', include('apps.home.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/olympiads/', include('apps.olympiads.api.urls', namespace='api-olympiads')),
    path('api/courses/', include('apps.courses.api.urls', namespace='api-courses')),
    path('api/students/', include('apps.students.api.urls', namespace='api-students')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
