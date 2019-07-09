import requests

from .config import WIKI_NB_SENTENCES
from .geoloc import Geoloc


class WikiSearch:
    WIKI_SEARCH_URL = "https://fr.wikipedia.org/w/api.php"
    WIKI_URL = "https://fr.wikipedia.org/?curid={}"

    @classmethod
    def page_id_text(cls, txt):
        params = {
            "action": "query",
            "list": "search",
            "srsearch": txt,
            "srnamespace": 0,
            "format": "json",
        }

        r = requests.get(cls.WIKI_SEARCH_URL, params=params)
        if r.status_code != 200:
            return False
        else:
            resp = r.json()
            if not len(resp["query"]["search"]):
                return False
            else:
                return resp["query"]["search"][0]["pageid"]

    @classmethod
    def page_id_coords(cls, coords):
        params = {
            "action": "query",
            "list": "geosearch",
            "gscoord": "{}|{}".format(coords[0], coords[1]),
            "gsradius": 10000,
            "gslimit": 10,
            "format": "json",
            "gsprop": "type|city",
            "gslimit": 100,
        }

        r = requests.get(cls.WIKI_SEARCH_URL, params=params)
        if r.status_code != 200:
            return False
        else:
            resp = r.json()

            places = resp["query"]["geosearch"]
            for p in places:
                if p["type"] == "city":
                    return p["pageid"]

    @classmethod
    def extract_from_pageid(cls, pageid=None):
        if pageid is not None:
            params = {
                "action": "query",
                "prop": "extracts",
                "exintro": 1,
                "exsentences": WIKI_NB_SENTENCES,
                "explaintext": 1,
                "redirects": 1,
                "pageids": pageid,
                "format": "json",
            }

            r = requests.get(cls.WIKI_SEARCH_URL, params=params)
            if r.status_code == 200:
                resp = r.json()

                return resp["query"]["pages"][str(pageid)]["extract"]
