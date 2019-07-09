import unicodedata
import string
import os
from pattern.fr import parsetree

from urllib.request import urlopen


class Parser:
    STOPWORDS_URL = "https://raw.githubusercontent.com/stopwords-iso/stopwords-fr/master/stopwords-fr.txt"
    STOPWORDS = ["salut", "bonjour", "grandpy", "grandpybot", "adresse"]

    def __new__(self, txt):
        tree = parsetree(txt)
        if not len(tree):
            return False
        else:
            sentence = tree[0]

        # if not sentence.is_question:
        #     return False

        relevant_nouns = [n for n in sentence.nouns if n.string not in self.STOPWORDS]
        if len(relevant_nouns):
            return relevant_nouns[-1].chunk.string
        else:
            return False
