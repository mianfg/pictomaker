from card import PictoCard
from language import PictoLanguage
from imagehandler import PictoImageHandler
from manager import PictoManager, PictoType

import random

class PictoInterface:
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
        'INTJ':     ((255,255,255), (0,0,0)),

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

    @staticmethod
    def tokens_to_cards(tokens):
        cards = []
        for token in tokens:
            print("searching " + token[1])
            print(token)
            picto_route = PictoManager.get_picto(token[1], PictoType.Color)
            print(picto_route)
            no_items = len(picto_route)
            print(no_items)
            if no_items > 0:
                select= random.randint(0, no_items-1)
                print("selected: "+str(select))
                picto_route = picto_route[select]
            else:
                picto_route = ""
            print("picto_route: " + picto_route)
            font_route = "../resources/font_sansserif.ttf"
            card = PictoCard(token[0], token[1], picto_route, \
                PictoInterface.color_map[token[2]][0], \
                PictoInterface.color_map[token[2]][1], \
                # native card dimensions
                (600, 750), 50, font_route, 60)
            cards.append(card)
        
        return cards

    @staticmethod
    def to_card(sentence):
        tokenized = PictoLanguage.tokenize(sentence)
        cards = PictoInterface.tokens_to_cards(tokenized)
        PictoImageHandler.generate_cards(cards)



PictoInterface.to_card("La teta de Javi es bonita.")