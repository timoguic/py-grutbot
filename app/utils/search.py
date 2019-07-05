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
        
    def process(self):
        coords = self._get_coords(self.input)
        output = {'coords': coords}

        if coords:
            wiki_pageid, wiki_url = self._get_wiki_info_from_coords(coords)
            output.update({'wiki_url': wiki_url})
            if wiki_pageid > 0:
                wiki_extract = self._get_wiki_intro_from_pageid(wiki_pageid)
                output.update({'wiki_extract': wiki_extract})

        return output

    @classmethod
    def _get_coords(cls, txt):
        params = {
            'q': txt,
            'format': 'json',
        }

        r = requests.get(cls.GEOCODE_URL, params=params)
        if r.status_code != 200:
            return False
        else:
            resp = r.json()
            if not len(resp):
                return False
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
                    return False

    @classmethod
    def _get_wiki_info_from_coords(cls, coords):
        params = {
            'action': "query",
            'list': "geosearch",
            'gscoord': '{}|{}'.format(coords[0], coords[1]),
            'gsradius': 10000,
            'gslimit': 10,
            'format': 'json',
            'gsprop': 'type|city',
            'gslimit': 100,
        }

        r = requests.get(cls.WIKI_SEARCH_URL, params=params)
        if r.status_code == 200:
            resp = r.json()

            places = resp['query']['geosearch']
            for p in places:
                if p['type'] == 'city':
                    wiki_pageid = p['pageid']
                    wiki_url = 'https://fr.wikipedia.org/?curid={}'.format(wiki_pageid)
                    return wiki_pageid, wiki_url

        return 0, False

    @classmethod
    def _get_wiki_intro_from_pageid(cls, pageid=None):
        if pageid is not None:
            params = {
                'action': 'query',
                'prop': 'extracts',
                'exintro': 1,
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
        return '<Search["{}", coords=({:2.4f}, {:2.4f})]>'.format(self.input, *self._get_coords())
        
if __name__ == "__main__":
    paris = Search('paris france')
    paris._get_coords()
    print(paris.coords)
 
    paris._get_wiki_info()
    print(paris.wiki_pageid, paris.wiki_url)

    paris._get_wiki_intro()
    print(paris.wiki_extract)