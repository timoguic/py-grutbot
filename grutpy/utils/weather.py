import requests

from .config import OPENWEATHER_API_KEY

class Weather:
	OWM_URL = 'http://api.openweathermap.org/data/2.5/weather'
	OWM_ICON_URL = 'http://openweathermap.org/img/wn/{}@2x.png'

	def __new__(self, coords):
		if type(coords) == tuple and len(coords) == 2:
			lat = coords[0]
			lon = coords[1]
		
		try:
			lat = float(lat)
			lon = float(lon)
		except ValueError:
			raise AttributeError('Please call with tuple (lat, lon) containing floats.')

		return self.get_data(lat, lon)

	@classmethod
	def get_data(cls, lat, lon):
		params = {
			'lat': lat,
			'lon': lon,
			'lang': 'fr',
			'units': 'metric',
			'APPID': OPENWEATHER_API_KEY,
		}
		r = requests.get(cls.OWM_URL, params=params)
		resp = r.json()
		
		if 'weather' not in resp.keys():
			return False
		
		description = resp['weather'][0]['description']
		temp = '{:.1f}'.format(resp['main']['temp'])
		icon = resp['weather'][0]['icon']
		return {
			'description': description,
			'temp': temp,
			'icon': cls.OWM_ICON_URL.format(icon),
		}