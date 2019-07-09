import os


def get_env_var(key, default=None):
    val = os.environ.get(key, None)
    if not val:
        if not default:
            raise RuntimeError("Cannot find env var {}.".format(key))
        else:
            return default
    else:
        return val


RAPID_API_KEY = get_env_var("RAPID_API_KEY")
OPENWEATHER_API_KEY = get_env_var("OWM_API_KEY")
WIKI_NB_SENTENCES = get_env_var("WIKI_NB_SENTENCES", 2)
