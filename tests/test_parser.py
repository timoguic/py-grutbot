from grutpy.utils import Parser

class TestParser:
    def setup(self):
        pass

    def test_parser(self):
        text = "bonjour grandpy parser  text, éééé --_[]{,; 123 le à de d' xz"
        self.parsed_text = Parser(text, filters=['shortwords', 'stopwords', 'punctuation', 'ascii', 'stopwords'])
        assert self.parsed_text == 'parser text eeee 123'

    def test_nlp(self):
        truc = Parser("""salut grandpy, quelle est l'adresse d'openclassrooms?""", filters=['nlp'])
        assert truc == 'openclassrooms'

        truc = Parser("""salut grandpy, ou se trouve la Tour Eiffel?""", filters=['nlp'])
        assert truc == 'la Tour Eiffel'

    def test_nlp_no_question(self):
        truc = Parser("""salut mon grand""", filters=['nlp'])
        assert type(truc) == bool and truc == False 