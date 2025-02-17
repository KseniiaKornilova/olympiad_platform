from django.urls import path

from . import views


app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('is_not_ready/', views.is_not_ready, name='is_not_ready'),
    path('set_language/<str:lang_code>/', views.set_language, name='set_language'),
]

handler404 = "apps.home.views.page_not_found"
