#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PictoManager
============

This module manages the resources (images).

"""


from enum import Enum
from os import listdir
from os.path import isfile, join, abspath


class PictoType(Enum):
    Color   = 1
    BnW     = 2
    Custom  = 3


class PictoManager:

    @staticmethod
    def __get_files(path):
        return [f for f in listdir(path) if isfile(join(path, f))]
    
    @staticmethod
    def __is_word(word, filename):
        return word.lower() == filename.split('.')[0].split('_')[0].lower()

    @staticmethod
    def get_picto(word):
        paths = []
        path = "./static/color"

        #if type == PictoType.Color:
        #    path = "../resources/color"
        #elif type == PictoType.BnW:
        #    path = "../resources/bnw"

        if path != "":
            files = PictoManager.__get_files(path)
            # WIP sinónimos
            for filename in files:
                if PictoManager.__is_word(word, filename):
                    paths.append(filename.split('.')[0])
        if len(paths) == 0:
            paths.append("/static/color/1")
        
        return paths
    
    @staticmethod
    def get_route(picto, type):
        path = ""

        if type == PictoType.Color:
            path = "./static/color"
        elif type == PictoType.BnW:
            path = "./static/bnw"
        
        if path != "":
            return abspath(join(path, picto + ".png"))