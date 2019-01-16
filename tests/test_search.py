from app.utils.search import Search

class TestSearch:
    def setup(self):
        self.paris = Search('paris france')
        self.nowhere = Search('this is nowhere to be found')

    def test_search_coords(self):
        assert self.paris._get_coords() == (48.8566101, 2.3514992)
        assert self.nowhere._get_coords() == (0, 0)

    def test_search_wiki(self):
        paris = self.paris.search()
        assert paris['wiki_url'] == 'https://fr.wikipedia.org/?curid=131365'
        assert paris['wiki_extract'] == "La place de l'Hôtel-de-Ville - Esplanade de la Libération, ancienne place de Grève jusqu'en 1803, est une place de Paris, en France."