#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


class PictoCard:
    def __init__(self, text, image_path, bg_color, gramm):
        self.__text = text
        self.__image_path = image_path
        self.__bg_color = bg_color      # html
        self.__gramm = gramm
    
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

    def get_gramm(self):
        return self.__gramm
    
    def set_gramm(self, gramm):
        self.__gramm = gramm

    def to_json(self):
        # create dict
        result = {
            "text" :            self.__text,
            "image_path" :      self.__image_path,
            "bg_color" :        self.__bg_color,
            "gramm" :      self.__gramm
        }

        return result #json.dumps(dict)
