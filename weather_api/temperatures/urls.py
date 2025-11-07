from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CityTemperatureViewSet

router = DefaultRouter()
router.register(r'temperatures', CityTemperatureViewSet, basename='temperature')

urlpatterns = [
    path('api/', include(router.urls)),
]
