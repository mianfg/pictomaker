import nltk, spacy
from nltk.tokenize import sent_tokenize
from manager import PictoManager


class PictoWord:
    POS = [
        'ADJ',      # adjective
        'ADP',      # adposition
        'ADV',      # adverb
        'AUX',      # auxiliary
        'CONJ',     # conjuction
        'CCONJ',    # coordinating conjunction
        'DET',      # determiner
        'INTJ',     # interjection
        'NOUN',     # noun
        'NUM',      # numeral
        'PART',     # particle
        'PRON',     # pronoun
        'PROPN',    # proper noun
        'PUNCT',    # punctuation
        'SCONJ',    # subordinating conjunction
        'SYM',      # symbol
        'VERB',     # verb
        'X',        # other
        'SPACE'     # space -- note: tokenizer deletes this
    ]

    MAP = {
        'ADJ' :     "ADJ",
        'ADP' :     "PREP",
        'ADV' :     "ADVERB",
        'AUX' :     "OTHER",
        'CONJ' :    "CONJ",
        'CCONJ' :   "CCONJ",
        'DET' :     "DET",
        'INTJ' :    "INTERJ",
        'NOUN' :    "SUST",
        'NUM' :     "PRON",
        'PART' :    "OTHER",
        'PRON' :    "PRON",
        'PROPN' :   "SUST",
        'PUNCT' :   "OTHER",
        'SCONJ' :   "CONJ",
        'SYM' :     "OTHER",
        'VERB' :    "VERB",
        'X' :       "OTHER",
        'SPACE' :   "OTHER"     # space -- note: tokenizer deletes this
    }

    def __init__(self, print, lemma, pos, picto=""):
        self.__print = print
        self.__lemma = lemma
        self.__pos = pos
        self.__picto = picto
    
    def get_print(self):
        return self.__print
    
    def set_print(self, print):
        self.__print = print
    
    def get_lemma(self):
        return self.__lemma
    
    def set_lemma(self, lemma):
        self.__lemma = lemma
    
    def get_pos(self):
        return PictoWord.MAP[self.__pos]
    
    def set_pos(self, pos):
        if pos not in PictoWord.POS:
            pos = 'X'
        
        self.__pos = pos


class PictoLanguage:
    def __init__(self):
        self.__NLP = spacy.load("es_core_news_sm") # WIP load before

    def tokenize(self, sentence):
        """
        Tokenizes sentence into an array of PictoWords:
        """

        # iterate over words
        nlp = self.__NLP(sentence)

        print_arr = sentence.split()
        lemma_arr = []
        pos_arr = []

        tokens = []

        for token in nlp:
            tokens.append((token.text, token.lemma_, token.pos_))
        
        print(tokens)

        i = 0
        for p in print_arr:
            lemma = ""
            pos = "X"

            iterate = True
            while iterate:
                if tokens[i][0] in p:
                    if tokens[i][2] != "PUNCT":
                        pos = tokens[i][2]
                        if pos == "VERB" or tokens[i][1][-2:] in ['ar','er','ir']:
                            lemma += tokens[i][1]
                        else:
                            lemma += tokens[i][0]
                    i += 1
                else:
                    iterate = False
                
                if i >= len(tokens):
                    iterate = False

            lemma_arr.append(lemma)
            pos_arr.append(pos)

        tokens = []

        for i in range(0, len(print_arr)):
            word = PictoWord(print_arr[i], lemma_arr[i], pos_arr[i])
            tokens.append(word)
        
        # WIP word grouping using (( ... ))

        return tokens



"""test
l = PictoLanguage()
print(l.tokenize("El pequeño ((Miguel Ángel)) quiere ir a su casa."))
"""