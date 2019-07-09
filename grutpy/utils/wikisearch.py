import requests

from .config import WIKI_NB_SENTENCES
from .geoloc import Geoloc


class WikiSearch:
    WIKI_SEARCH_URL = 'https://fr.wikipedia.org/w/api.php'
    WIKI_URL = 'https://fr.wikipedia.org/?curid={}'

    NOT_FOUND = ('NOT_FOUND', 'NOT_FOUND')

    def __init__(self, txt, coords=None):
        self.input = txt

        if not coords:
            coords = Geoloc(txt)
            self.coords = coords
        else:
            self.coords = coords

        self._page_id_text = None
        self._page_id_coords = None
        self._extract = None

    @property
    def url(self):
        if self.page_id_coords > 0:
            pageid = self.page_id_coords
        elif self.page_id_text > 0:
            pageid = self.page_id_text
        else:
            pageid = 0

        if pageid > 0:
            return self.WIKI_URL.format(pageid)
        else:
            return False

    @property
    def extract(self):
        if self._extract:
            return self._extract

        if self.page_id_coords > 0:
            extract = self.extract_from_pageid(self.page_id_coords)
        elif self.page_id_text > 0:
            extract = self.extract_from_pageid(self.page_id_text)
        else:
            extract = False
        
        self._extract = extract
        return self._extract

    @property
    def page_id_text(self):
        if self._page_id_text:
            return self._page_id_text

        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': self.input,
            'srnamespace': 0,
            'format': 'json',
        }

        r = requests.get(self.WIKI_SEARCH_URL, params=params)
        if r.status_code != 200:
            return False
        else:
            resp = r.json()
            if not len(resp['query']['search']):
                return False
            else:
                self._page_id_text = resp['query']['search'][0]['pageid']
                return self._page_id_text
            
    @property
    def page_id_coords(self):
        if self._page_id_coords:
            return self._page_id_coords

        params = {
            'action': "query",
            'list': "geosearch",
            'gscoord': '{}|{}'.format(self.coords[0], self.coords[1]),
            'gsradius': 10000,
            'gslimit': 10,
            'format': 'json',
            'gsprop': 'type|city',
            'gslimit': 100,
        }

        r = requests.get(self.WIKI_SEARCH_URL, params=params)
        if r.status_code != 200:
            return False
        else:
            resp = r.json()

            places = resp['query']['geosearch']
            for p in places:
                if p['type'] == 'city':
                    self._page_id_coords = p['pageid']
                    return self._page_id_coords

    @classmethod
    def extract_from_pageid(cls, pageid=None):
        if pageid is not None:
            params = {
                'action': 'query',
                'prop': 'extracts',
                'exintro': 1,
                'exsentences': WIKI_NB_SENTENCES,
                'explaintext': 1,
                'redirects': 1,
                'pageids': pageid,
                'format': 'json',
            }

            r = requests.get(cls.WIKI_SEARCH_URL, params=params)
            if r.status_code == 200:
                resp = r.json()

                return resp['query']['pages'][str(pageid)]['extract']

    def __str__(self):
        return "<WikiSearch['{}', ({:2.4f},{:2.4f})]>".format(self.input, *self.coords)
