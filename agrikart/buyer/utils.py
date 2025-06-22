import random

def generate_random_lat_lon(base_lat=28.6139, base_lon=77.2090, spread_km=5):
    """Generate random lat/lon within ~5km of a base location (default: Delhi)."""
    delta = spread_km / 111  # Roughly convert km to degrees
    lat = base_lat + random.uniform(-delta, delta)
    lon = base_lon + random.uniform(-delta, delta)
    return round(lat, 6), round(lon, 6)
