#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


class PictoCard:
    def __init__(self, text, image_path, bg_color, text_color):
        self.__text = text
        self.__image_path = image_path
        self.__bg_color = bg_color      # (R,G,B)
        self.__text_color = text_color  # (R,G,B)
    
    def get_text(self):
        return self.__text
    
    def set_text(self, text):
        self.__text = text

    def get_image_path(self):
        return self.__image_path

    def set_image_path(self, image_path):
        self.__image_path = image_path
    
    def get_bg_color(self):
        return self.__bg_color
    
    def set_bg_color(self, bg_color):
        self.__bg_color = bg_color

    def get_text_color(self):
        return self.__text_color
    
    def set_text_color(self, text_color):
        self.__text_color = text_color

    def to_json(self):
        # create dict
        result = {
            "text" :            self.__text,
            "image_path" :      self.__image_path,
            "bg_color" :        self.__bg_color,
            "text_color" :      self.__text_color
        }

        return result #json.dumps(dict)
