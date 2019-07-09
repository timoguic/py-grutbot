from grutpy.utils import Parser


class TestParser:
    def setup(self):
        pass

    def test_nlp(self):
        truc = Parser("""salut grandpy, quelle est l'adresse d'openclassrooms?""")
        assert truc == "openclassrooms"

        truc = Parser("""salut grandpy, ou se trouve la Tour Eiffel?""")
        assert truc == "la Tour Eiffel"
