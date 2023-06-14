from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShortenerListAPIView
import  api 

router = DefaultRouter()
router.register(r'links', ShortenerListAPIView, basename='link')

urlpatterns = [
    # Other URL patterns
    path('', include(router.urls)),
    path('api/', include(api.urls)),
    path('create-link/', ShortenerListAPIView.as_view({'post': 'create'}), name='create_link'),
    # ...
]
