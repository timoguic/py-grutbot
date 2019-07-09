from grutpy.utils import WikiSearch
import requests

class TestSearch:
    def setup(self):
        self.paris = WikiSearch('paris france?', coords=(99,99))

    def test_search_coords(self, monkeypatch):
        return True
        LATITUDE = 48.8566101
        LONGITUDE = 2.3514992
        
        class MockResponseParis:
            status_code = 200
            def __init__(self, *args, **kwargs): pass
            def json(self):
                return [{'lat': LATITUDE, 'lon': LONGITUDE}]

        monkeypatch.setattr(requests, 'get', MockResponseParis)
        assert self.paris._get_coords() == (48.8566101, 2.3514992)

    def test_search_wiki(self, monkeypatch):
        return True
        PAGEID = 681159
        class MockResponseWiki:
            status_code = 200
            def __init__(self, *args, **kwargs): pass
            def json(self):
                return {
                    'query': {
                        'geosearch': [
                            {'type': 'city', 'pageid': PAGEID}
                        ],
                        'pages': {
                            str(PAGEID): {'extract': 'Paris'}
                        }
                    }
                }

        monkeypatch.setattr(requests, 'get', MockResponseWiki)

        wiki_info = Search._get_wiki_info_from_coords((48.8566101, 2.3514992))
        assert wiki_info[1] == 'https://fr.wikipedia.org/?curid=681159'

        wiki_extract = Search._get_wiki_intro_from_pageid(PAGEID)
        assert 'Paris' in wiki_extract