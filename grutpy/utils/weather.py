import requests

from .config import OPENWEATHER_API_KEY

class Weather:
	OWM_URL = 'http://api.openweathermap.org/data/2.5/weather'
	OWM_ICON_URL = 'http://openweathermap.org/img/wn/{}@2x.png'

	def __new__(self, *args, **kwargs):
		if len(args) == 1 and type(args[0]) == tuple and len(args[0]) == 2:
			lat = args[0][0]
			lon = args[0][1]
		elif 'lat' in kwargs.keys() and 'lon' in kwargs.keys():
			lat = kwargs['lat']
			lon = kwargs['lon']
		else:
			lat = 'Nan'
			lon = 'Nan'

		try:
			lat = float(lat)
			lon = float(lon)
		except ValueError:
			raise AttributeError('Please call with tuple(lat, lon) or keyword arguments (lat=, lon=)')

		return self.get_data(lat, lon)

	@classmethod
	def get_data(cls, lat, lon):
		print(OPENWEATHER_API_KEY)
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
			return {'weather_description': False, 'weather_icon': False}
		
		description = resp['weather'][0]['description']
		temp = '{:.1f}'.format(resp['main']['temp'])
		icon = resp['weather'][0]['icon']
		return {
			'weather_description': description,
			'weather_temp': temp,
			'weather_icon': cls.OWM_ICON_URL.format(icon),
		}