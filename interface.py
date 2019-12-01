from card import PictoCard
from language import PictoLanguage
from imagehandler import PictoImageHandler
from manager import PictoManager, PictoType

import random


class PictoInterface():
    color_map = {
        # adjective
        'ADJ':      ((255,255,255), (0,0,0)),
        
        # adposition
        'ADP':      ((255,255,255), (0,0,0)),

        # adverb
        'ADV':      ((255,255,255), (0,0,0)),

        # auxiliary
        'AUX':      ((255,255,255), (0,0,0)),

        # conjunction
        'CONJ':     ((255,255,255), (0,0,0)),

        # coordinating conjunction
        'CCONJ':    ((255,255,255), (0,0,0)),

        # determiner
        'DET':      ((219,0,0), (255,255,255)),

        # interjection
        'INTJ':     ((0,0,255), (0,0,0)),

        # noun
        'NOUN':     ((0,0,0), (255,255,255)),

        # numeral
        'NUM':      ((255,255,255), (0,0,0)),

        # particle
        'PART':     ((255,255,255), (0,0,0)),

        # pronoun
        'PRON':     ((255,255,255), (0,0,0)),

        # proper noun
        'PROPN':    ((255,255,255), (0,0,0)),

        # punctuation
        'PUNCT':    ((255,255,255), (0,0,0)),

        # subordinating conjunction
        'SCONJ':    ((255,255,255), (0,0,0)),

        # symbol
        'SYM':      ((255,255,255), (0,0,0)),

        # verb
        'VERB':     ((255,255,255), (0,0,0)),

        # other
        'X':        ((255,255,255), (0,0,0)),

        # space -- note: tokenizer deletes this
        'SPACE':    ((255,255,255), (0,0,0))
    }

    def __init__(self, language, image_handler):
        self.__language = language
        self.__image_handler = image_handler

    def get_config(self):
        pass    # devolver valores de colores

    def new_cards(self):
        pass

    def tokens_to_cards(self, tokens):
        cards = []
        for token in tokens:
            picto_route = PictoManager.get_picto(token.get_lemma())#, PictoType.Color)
            no_items = len(picto_route)
            if no_items > 0:
                select = random.randint(0, no_items-1)
                picto_route = picto_route[select]
            else:
                picto_route = ""
            
            picto_route = PictoManager.get_route(picto_route, PictoType.Color)
            card = PictoCard(token.get_print(), \
                picto_route, \
                PictoInterface.color_map[token.get_pos()][0], \
                PictoInterface.color_map[token.get_pos()][1])
            
            cards.append(card)
        
        return cards

    def to_card(self, sentence):
        tokenized = self.__language.tokenize(sentence)
        cards = self.tokens_to_cards(tokenized)
        self.__image_handler.generate_cards(cards)
    
    def get_cards(self, sentence):
        tokenized = self.__language.tokenize(sentence)
        return self.tokens_to_cards(tokenized)