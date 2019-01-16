import requests

class Search:
    GEOCODE_URL = 'https://nominatim.openstreetmap.org/search'
    WIKI_SEARCH_URL = 'https://fr.wikipedia.org/w/api.php'

    NOT_FOUND = ('NOT_FOUND', 'NOT_FOUND')

    def __init__(self, txt):
        self.input = txt
        self.coords = (0, 0)
        self.wiki_pageid = None
        self.wiki_url = None
        self.wiki_extract = None
        
    def search(self):
        self._get_coords()
        self._get_wiki_info()
        self._get_wiki_intro()

        return {'coords': self.coords, 'wiki_url': self.wiki_url, 'wiki_extract': self.wiki_extract}

    def _get_coords(self):
        params = {
            'q': self.input,
            'format': 'json',
        }

        r = requests.get(self.GEOCODE_URL, params=params)
        if r.status_code == 200:
            resp = r.json()
            if len(resp):
                resp = resp[0]

                lat = resp.get('lat', None)
                lng = resp.get('lon', None)

                if lat and lng:
                    try:
                        lat = float(lat)
                        lng = float(lng)
                    except ValueError:
                        pass
                    
                    self.coords = (lat, lng)

        return self.coords

    def _get_wiki_info(self):
        if self.coords is not (0, 0):
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
            if r.status_code == 200:
                resp = r.json()

                places = resp['query']['geosearch']
                for p in places:
                    if p['type'] == 'city':
                        self.wiki_pageid = p['pageid']
                        self.wiki_url = 'https://fr.wikipedia.org/?curid={}'.format(self.wiki_pageid)
                        return True

            return False

    def _get_wiki_intro(self):
        if self.wiki_pageid is not None:
            params = {
                'action': 'query',
                'prop': 'extracts',
                'exintro': 1,
                'explaintext': 1,
                'redirects': 1,
                'pageids': self.wiki_pageid,
                'format': 'json',
            }

            r = requests.get(self.WIKI_SEARCH_URL, params=params)
            if r.status_code == 200:
                resp = r.json()

                extract = resp['query']['pages'][str(self.wiki_pageid)]['extract']
                self.wiki_extract = extract
        
if __name__ == "__main__":
    paris = Search('paris france')
    paris._get_coords()
    print(paris.coords)
 
    paris._get_wiki_info()
    print(paris.wiki_pageid, paris.wiki_url)

    paris._get_wiki_intro()
    print(paris.wiki_extract)