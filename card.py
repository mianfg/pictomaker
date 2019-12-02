#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


class PictoCard:
    def __init__(self, text, image_path, gramm):
        self.__text = text
        self.__image_path = image_path
        self.__gramm = gramm
    
    def get_text(self):
        return self.__text
    
    def set_text(self, text):
        self.__text = text

    def get_image_path(self):
        return self.__image_path

    def set_image_path(self, image_path):
        self.__image_path = image_path

    def get_gramm(self):
        return self.__gramm
    
    def set_gramm(self, gramm):
        self.__gramm = gramm

    def to_json(self):
        # create dict
        result = {
            "text" :            self.__text,
            "image_path" :      self.__image_path,
            "gramm" :      self.__gramm
        }

        return result #json.dumps(dict)
