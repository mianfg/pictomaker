#!/usr/bin/env python
# -*- coding: utf-8 -*-


class PictoCard:
    
    def __init__(self, word, lemma, picto_route, bg_color, text_color, \
        card_dimensions, picto_margin, text_font_route, text_size):
        # ROUTES ARE ABSOLUTE
        self.__word = word
        self.__lemma = lemma
        self.__picto_route = picto_route
        self.__text_color = text_color
        self.__bg_color = bg_color
        self.__card_dimensions = card_dimensions
        self.__picto_margin = picto_margin
        self.__text_font_route = text_font_route
        self.__text_size = text_size
    
    def get_word(self):
        return self.__word
    
    def set_word(self, word):
        self.__word = word
    
    def get_lemma(self):
        return self.__lemma
    
    def set_lemma(self, lemma):
        self.__lemma = lemma
    
    def get_picto_route(self):
        return self.__picto_route
    
    def set_picto_route(self, picto_route):
        self.__picto_route = picto_route
    
    def get_text_color(self):
        return self.__text_color
    
    def set_text_color(self, text_color):
        self.__text_color = text_color
    
    def get_bg_color(self):
        return self.__bg_color
    
    def set_bg_color(self, bg_color):
        self.__bg_color = bg_color

    def get_card_dimensions(self):
        return self.__card_dimensions

    def set_card_dimensions(self, card_dimensions):
        self.__card_dimensions = card_dimensions
    
    def get_picto_margin(self):
        return self.__picto_margin
    
    def set_picto_margin(self, picto_margin):
        self.__picto_margin = picto_margin
    
    def get_text_font_route(self):
        return self.__text_font_route
    
    def set_text_font_route(self, text_font_route):
        self.__text_font_route = text_font_route

    def get_text_size(self):
        return self.__text_size
    
    def set_text_size(self, text_size):
        self.__text_size = text_size