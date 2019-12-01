#!/usr/bin/env python
# -*- coding: utf-8 -*-

from manager import PictoManager, PictoType
from language import PictoLanguage
from PIL import Image, ImageOps, ImageDraw, ImageFont


class PictoImageHandler:
    def __init__(self, font, text_size, card_dimensions, image_margin):
        self.__font = font
        self.__text_size = text_size
        self.__card_dimensions = card_dimensions
        self.__image_margin = image_margin

    def generate_card(self, card):
        card_width, card_height = self.__card_dimensions
        image_margin = self.__image_margin
        image_dimensions = card_width - image_margin*2
        image_dimensions = (image_dimensions, image_dimensions)

        text = card.get_text()
        image_path = card.get_image_path()
        bg_color = card.get_bg_color()
        text_color = card.get_text_color()

        img = Image.new('RGB', (card_width, card_height), (255, 255, 255))
        
        draw = ImageDraw.Draw(img)
        draw.rectangle([(50,50), (550,700)], fill=bg_color)
        draw.rectangle([(55,55), (545,695)], fill=(255,255,255))

        try:
            picto = Image.open(image_path, 'r')
        except:
            picto = Image.new('RGB', (card_width, card_height), bg_color)
        
        picto = picto.resize(image_dimensions)
        img.paste(picto, (image_margin, image_margin))

        
        text_font = ImageFont.truetype(self.__font, self.__text_size)
        text_width, text_height = draw.textsize(text, font=text_font)
        draw.text((int((card_width-text_width)/2), image_margin*2 + image_dimensions[0]), text, text_color, font=text_font)

        output_path = "../generated/" + text + "_generated.png"
        img.save(output_path)
        return output_path
    
    def generate_cards(self, cards, join=False):
        """
        Important: card dimensions should be the same for every card
        """

        length = len(cards)
        _, cards_height = self.__card_dimensions

        if join:
            cards_width = self.__image_margin + (self.__card_dimensions[0] - self.__image_margin)*length
            cards_repeat = self.__card_dimensions[0] - self.__image_margin
        else:
            cards_width = self.__card_dimensions[0]*length
            cards_repeat = self.__card_dimensions
        
        card_routes = []
        for c in cards:
            card_routes.append(self.generate_card(c))
        
        img = Image.new('RGB', (cards_width, cards_height), 255)
        i = 0
        for r in card_routes:
            card_img = Image.open(r)
            img.paste(card_img, (i*cards_repeat, 0))
            i += 1

        output_route = "../generated/cards_generated.png"
        img.save(output_route)
        return output_route
