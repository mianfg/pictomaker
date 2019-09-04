#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fpdf import FPDF


"""pdf = FPDF(orientation='P', unit='pt', format=(500,600))
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.image('/home/mianfg/Proyectos/picto/resources/color/sentar en el borde.png', x=50, y=50, w=400, h=400)
pdf.cell(500, 520, txt="Welcome to Python!", ln=1, align="C")

pdf.output("simple_demo.pdf")"""

from manager import PictoManager, PictoType
from language import PictoLanguage
from PIL import Image, ImageOps, ImageDraw, ImageFont


class PictoImageHandler:
    @staticmethod
    def generate_card(card):
        card_width, card_height = card.get_card_dimensions()
        image_margin = card.get_picto_margin()
        image_dimensions = card_width - image_margin*2
        image_dimensions = (image_dimensions, image_dimensions)

        word = card.get_word()

        back_color = card.get_bg_color()
        text_color = card.get_text_color()

        img = Image.new('RGB', (card_width, card_height), back_color)
        try:
            picto = Image.open(card.get_picto_route(), 'r')
        except:
            picto = Image.new('RGB', image_dimensions, back_color)
        
        picto = picto.resize(image_dimensions)
        img.paste(picto, (image_margin, image_margin))
        
        draw = ImageDraw.Draw(img)
        text_font = ImageFont.truetype(card.get_text_font_route(), card.get_text_size())
        text_width, text_height = draw.textsize(word, font=text_font)
        draw.text((int((card_width-text_width)/2), card_height - image_margin - text_height), word, text_color, font=text_font)
        
        output_route = word + "_generated.png"
        img.save(output_route)
        return output_route
    
    @staticmethod
    def generate_cards(cards, join=False):
        """
        Important: card dimensions should be the same for every card
        """

        length = len(cards)
        card = cards[0] # to get dimensions -- see specification

        _, cards_height = card.get_card_dimensions()

        if join:
            cards_width = card.get_picto_margin() + (card.get_card_dimensions()[0] - card.get_picto_margin)*length
            cards_repeat = card.get_card_dimensions()[0] - card.get_picto_margin
        else:
            cards_width = card.get_card_dimensions()[0]*length
            cards_repeat = card.get_card_dimensions()[0]
        
        card_routes = []
        for c in cards:
            card_routes.append(PictoImageHandler.generate_card(c))
        
        img = Image.new('RGB', (cards_width, cards_height), 255)
        i = 0
        for r in card_routes:
            card_img = Image.open(r)
            img.paste(card_img, (i*cards_repeat, 0))
            i += 1
        
        # WIP write route
        output_route = "cards_generated.png"
        img.save(output_route)
        return output_route