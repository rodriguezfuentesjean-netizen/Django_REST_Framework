from django.db import models
from decimal import Decimal

class CityTemperature(models.Model):
    city = models.CharField(max_length=100, unique=True)
    # Ajusta max_digits/decimal_places según el rango que necesites
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} — {self.temperature}"

