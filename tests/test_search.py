from grutpy.utils import WikiSearch
import requests


class TestSearch:
    def test_search_wiki(self, monkeypatch):
        PAGEID = 681159

        class MockResponseWiki:
            status_code = 200

            def __init__(self, *args, **kwargs):
                pass

            def json(self):
                return {
                    "query": {
                        "geosearch": [{"type": "city", "pageid": PAGEID}],
                        "pages": {str(PAGEID): {"extract": "Paris"}},
                    }
                }

        monkeypatch.setattr(requests, "get", MockResponseWiki)

        assert WikiSearch.page_id_coords((48.8566101, 2.3514992)) == PAGEID
        assert "Paris" in WikiSearch.extract_from_pageid(PAGEID)
