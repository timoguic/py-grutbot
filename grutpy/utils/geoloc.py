import requests


class Geoloc:
    GEOCODE_URL = 'https://nominatim.openstreetmap.org/search'
    
    def __new__(self, txt):
        params = {
            'q': txt,
            'format': 'json',
        }

        r = requests.get(self.GEOCODE_URL, params=params)
        if r.status_code != 200:
            return None
        else:
            resp = r.json()
            if not len(resp):
                return None
            else:
                resp = resp[0]

                lat = resp.get('lat', None)
                lng = resp.get('lon', None)

                if lat and lng:
                    try:
                        lat = float(lat)
                        lng = float(lng)
                    except ValueError:
                        lat = 0
                        lng = 0
                    return lat, lng
                else:
                    return None