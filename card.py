#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PictoCard
=========

This module represents a pictogram card
"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2019, Bloomgogo"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "GPL"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "mianfg@bloomgogo.com"
__status__      = "Production"


# Python libary imports
import json


class PictoCard:
    """
    Class used to represent pictogram card's data

    ...

    Attributes
    ----------
    __text : str
        Card text
    __image_path : str
        Card image path, relative to static path
    __gramm : str
        Syntactical category, from a list of categories
        See language.py for categories list
    
    Methods
    -------
    get_text()
        Returns card text
    set_text(text)
        Sets card text
    get_image_path()
        Returns image path, relative to static path
    set_image_path()
        Sets image path, relative to static path
    get_gramm()
        Returns card's syntactical category
    set_gramm(gramm)
        Sets card's syntactical category
    to_dict()
        Returns card as Python dictionary

    """
    def __init__(self, text, image_path, gramm):
        """
        Parameters
        ----------
        text : str
            Card text
        image_path : str
            Card image path, relative to static path
        gramm : str
            Card syntactical category, from list of categories
            See language.py for list of categories
        """
        self.__text = text
        self.__image_path = image_path
        self.__gramm = gramm
    
    def get_text(self):
        """Returns card text

        Return
        ------
        str
            Card text
        """
        return self.__text
    
    def set_text(self, text):
        """Sets card text

        Parameters
        ----------
        text : str
            Card text
        """
        self.__text = text

    def get_image_path(self):
        """Returns image path

        Image path is returned relative to static path, specified in app.js

        Return
        ------
        str
            Image path
        """
        return self.__image_path

    def set_image_path(self, image_path):
        """Sets image path

        Image path must be set relative to static path

        Parameters
        ----------
        image_path : str
            Image path

        """
        self.__image_path = image_path

    def get_gramm(self):
        """Returns card's syntactical category

        Syntactical category from list of available categories
        See PictoLanguage for more details

        Return
        ------
        str
            Card's syntactical category
        """
        return self.__gramm
    
    def set_gramm(self, gramm):
        """Sets card's syntactical category

        Syntactical category must be from list of available categories
        See PictoLanguage for more details

        Parameters
        ----------
        gramm : str
            Syntactical category
        """
        self.__gramm = gramm

    def to_dict(self):
        """Returns card as Python dictionary

        The dictionary will be of the form:

        {
            "text" :        card text (str),
            "image_path" :  card image path (str),
            "gramm" :       card syntactical category (str)
        }

        Return
        ------
        dict
            As specified above
        """
        # create dict
        result = {
            "text" :       self.__text,
            "image_path" : self.__image_path,
            "gramm" :      self.__gramm
        }

        return result
