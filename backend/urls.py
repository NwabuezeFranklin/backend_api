# backend/urls.py

from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from App.views import Redirector
from api import views
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
    path('',include('App.urls')),
    path('<str:shortener_link>',Redirector.as_view(),name='redirector'),
    path('auth/',include('drf_social_oauth2.urls',namespace='drf')),
    path('accounts/', include('allauth.urls')),
    path('google/login/callback/', views.google_login_callback, name='google_login_callback'),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    # path("ckeditor5/", include('django_ckeditor_5.urls')),

]


urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

