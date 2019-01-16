import unicodedata
import string
from app.utils.stopwords import STOPWORDS

class Parser:
    
    def __init__(self, txt):
        self.input = txt
        self.output = None

    def parse(self):
        self.output = self._to_ascii(
            self._remove_stopwords(
                self._remove_punctuation(
                    self.input
                )
            )
        )
        return self.output

    @classmethod
    def _remove_punctuation(cls, txt):
        return txt.translate(str.maketrans("","", string.punctuation))

    @classmethod
    def _remove_stopwords(cls, txt):
        return ' '.join([
            w for w in txt.split()
            if w not in STOPWORDS
        ])

    @classmethod
    def _to_ascii(cls, txt):
        return unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore').decode()