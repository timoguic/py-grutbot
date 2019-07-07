import os

def get_env_var(key):
	val = os.environ.get(key)
	if not val:
		raise RuntimeError('Cannot find env var {}.'.format(key))
	else:
		return val

RAPID_API_KEY = get_env_var('RAPID_API_KEY')
OPENWEATHER_API_KEY = get_env_var('OWM_API_KEY')
