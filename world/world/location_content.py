import json
import requests
from math import cos


# Make bounding box (south, west, north, east)
# Latitude: 1 deg = 110.574 km
# Longitude: 1 deg = 111.320*cos(latitude) km
center_lat = 42.376980
center_lat_rad = center_lat * 3.14159265358979 / 180.
center_lon = -71.184400
offset_lat = (0.5 / 110.574)
offset_lon = (0.5 / (111.320 * cos(center_lat_rad)))

# Make a 1km box around the center point
# e.g. pubs in London (53.2987342,-6.3870259,53.4105416,-6.1148829)
bounding_box = (center_lat - offset_lat, center_lon - offset_lon,
                center_lat + offset_lat, center_lon + offset_lon)

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = f'[out:json];(node["amenity"]{bounding_box};way["amenity"]{bounding_box};relation["amenity"]{bounding_box};);out;'
print(overpass_query)
response = requests.get(overpass_url, params={'data': overpass_query})
data = response.json()

print(json.dumps(data, indent=4, sort_keys=True))
