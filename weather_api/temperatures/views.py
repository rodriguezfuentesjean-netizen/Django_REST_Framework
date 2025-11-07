from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import CityTemperature
from .serializers import CityTemperatureSerializer

class CityTemperatureViewSet(viewsets.ModelViewSet):
    queryset = CityTemperature.objects.all().order_by('city')
    serializer_class = CityTemperatureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # Si quieres controlar autenticación sólo aquí, puedes definir:
    # from rest_framework.authentication import TokenAuthentication
    # authentication_classes = [TokenAuthentication]

