#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PictoManager
============

This module manages the resources (images).

"""


def parse_info():
    with open("./static/index.txt") as f:
        content = f.readlines()
    
    content = [x.strip() for x in content]
    return content


class PictoManager:
    FILES = parse_info()
    
    @staticmethod
    def __is_word(word, filename):
        return word.lower() == filename.split('.')[0].split('_')[0].lower()

    @staticmethod
    def get_picto(word, append_default=True):
        paths = []
        default_image = "NOTFOUND.png"

        for filename in PictoManager.FILES:
            if PictoManager.__is_word(word, filename):
                paths.append(filename)
        
        if len(paths) == 0 and append_default:
            paths.append(default_image)
        
        paths.sort()
        
        return paths