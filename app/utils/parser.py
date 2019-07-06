import unicodedata
import string
import os
from pattern.fr import parsetree

from urllib.request import urlopen

class Parser:

    STOPWORDS_URL = 'https://raw.githubusercontent.com/stopwords-iso/stopwords-fr/master/stopwords-fr.txt'

    def __new__(cls, txt, filters=['nlp']):
    #def __new__(cls, txt, filters=['shortwords', 'stopwords', 'punctuation', 'ascii', 'stopwords']):
        output = txt
        func_prefixes = ['', '_', '_remove_', '_to_', '_run_']
        for f in filters:
            for pfx in func_prefixes:
                func = getattr(cls, pfx + f, None)
                if callable(func):
                    output = func(output)
                    break

        return output

    @classmethod
    def _remove_shortwords(cls, txt):
        return ' '.join([word for word in txt.split() if len(word) > 2])
        
    @classmethod
    def _remove_punctuation(cls, txt):
        return txt.translate(str.maketrans("","", string.punctuation))

    @classmethod
    def _remove_stopwords(cls, txt):
        stopwords = cls._load_stopwords()
        return ' '.join([
            w for w in txt.split()
            if w not in stopwords
        ])

    @classmethod
    def _to_ascii(cls, txt):
        return unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore').decode()

    @classmethod
    def _load_stopwords(cls):
        if not os.path.isdir('data'):
            os.makedirs('data')
        
        try:
            fp = open('data/stopwords.txt', 'r')
        except FileNotFoundError:
            stopwords = cls._download_stopwords()
        else:
            with fp:
                lines = fp.readlines()
                stopwords = [l.strip() for l in lines] if len(lines) else cls._download_stopwords()

        stopwords += ['salut', 'bonjour', 'grandpy', 'adresse']
        return stopwords

    @classmethod
    def _download_stopwords(cls):
        with urlopen(cls.STOPWORDS_URL) as req:
            if not req.getcode() == 200:
                print('Error getting stopwords from GitHub.')
            else:
                fp = open('data/stopwords.txt', 'w')
                fp.write(req.read().decode())

    @classmethod
    def _run_nlp(cls, txt):
        tree = parsetree(txt)
        if not len(tree):
            return False
        else:
            sentence = tree[0]

        if not sentence.is_question:
            return False
        
        stopwords = cls._load_stopwords()

        relevant_nouns = [n for n in sentence.nouns if n.string not in stopwords]
        if len(relevant_nouns):
            return relevant_nouns[-1].chunk.string
        else:
            return False