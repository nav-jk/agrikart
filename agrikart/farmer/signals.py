import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Farmer

@receiver(post_save, sender=Farmer)
def geocode_farmer_address(sender, instance, created, **kwargs):
    if (created or instance.latitude is None) and instance.address:
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': instance.address,
                'format': 'json'
            }
            response = requests.get(url, params=params).json()
            if response:
                instance.latitude = float(response[0]['lat'])
                instance.longitude = float(response[0]['lon'])
                instance.save()
        except Exception as e:
            print(f"Geocoding failed: {e}")
