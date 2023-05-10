import requests
import json
from django.utils.encoding import smart_str
from django.conf import settings
from typing import Optional

def get_lat_lng(location:str) -> tuple[Optional[str], Optional[str]]:
    """
    This function queries the google geocode api and returns the latlng coordinates in a tupple or a tuple of none
    """
    location = smart_str(location)
    key = settings.GOOGLE_API

    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={key}&sensor=false'
    response = requests.get(url)
    if response.status_code == 200:
        results = json.loads(response.text)
        status = results['status']
        if status == 'ZERO_RESULTS':
            return (None, None)
        elif status == 'OK':
            location = results['results'][0]['geometry']['location']
            print(location)
            lat, lng= location['lat'], location['lng']
            return (lat, lng)
    return (None, None)