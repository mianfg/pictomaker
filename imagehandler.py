#!/usr/bin/env python
# -*- coding: utf-8 -*-

from manager import PictoManager, PictoType
from language import PictoLanguage
from PIL import Image, ImageOps, ImageDraw, ImageFont
from io import BytesIO
import urllib.request
import requests

import uuid, zipfile, os


class PictoImageHandler:
    def __init__(self, font, text_size, card_dimensions, image_margin, base_path):
        self.__font = font
        self.__text_size = text_size
        self.__card_dimensions = card_dimensions
        self.__image_margin = image_margin
        self.__base_path = base_path

    def generate_card(self, card):
        card_width, card_height = self.__card_dimensions
        image_margin = self.__image_margin
        image_dimensions = card_width - image_margin*2
        image_dimensions = (image_dimensions, image_dimensions)

        text = card.get_text()
        image_path = card.get_image_path()
        bg_color = card.get_bg_color() #bg_color is color
        text_color = (0,0,0)

        img = Image.new('RGB', (card_width, card_height), (255, 255, 255))
        
        draw = ImageDraw.Draw(img)
        draw.rectangle([(self.__image_margin/2,self.__image_margin/2), (self.__card_dimensions[0]-self.__image_margin/2,self.__card_dimensions[1]-self.__image_margin/2)], fill=bg_color)
        draw.rectangle([(self.__image_margin,self.__image_margin), (self.__card_dimensions[0]-self.__image_margin,self.__card_dimensions[1]-self.__image_margin)], fill=(255,255,255))

        try:
            picto = Image.open(image_path, 'r')
        except:
            picto = Image.new('RGB', (card_width, card_height), bg_color)
        
        picto = picto.resize(image_dimensions)
        img.paste(picto, (image_margin, image_margin))

        
        text_font = ImageFont.truetype(self.__font, self.__text_size)
        text_width, text_height = draw.textsize(text, font=text_font)
        draw.text((int((card_width-text_width)/2), image_margin*2 + image_dimensions[0]), text, text_color, font=text_font)

        bytes_io = BytesIO()
        img.save(bytes_io, "PNG")
        return bytes_io
    
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

        bytes_io = BytesIO()
        img.save(bytes_io, "PNG")
        return bytes_io

    def generate_card2(self, text, color, image_url):
        card_width, card_height = self.__card_dimensions
        image_margin = self.__image_margin
        image_dimensions = card_width - image_margin*2
        image_dimensions = (image_dimensions, image_dimensions)

        text_color = (0,0,0)

        img = Image.new('RGB', (card_width, card_height), (255, 255, 255))

        try:
            picto = Image.open(requests.get(image_url, stream=True).raw)
        except:
            picto = Image.new('RGB', (card_width, card_height), (255,255,255))
        
        draw = ImageDraw.Draw(img)
        draw.rectangle([(self.__image_margin/4,self.__image_margin/4), (self.__card_dimensions[0]-self.__image_margin/4,self.__card_dimensions[1]-self.__image_margin/4)], fill=color)
        draw.rectangle([(3*self.__image_margin/4,3*self.__image_margin/4), (self.__card_dimensions[0]-3*self.__image_margin/4,self.__card_dimensions[1]-3*self.__image_margin/4)], fill=(255,255,255))

        picto = picto.resize(image_dimensions)
        img.paste(picto, (image_margin, image_margin))

        text_font = ImageFont.truetype(self.__font, self.__text_size)
        text_width, text_height = draw.textsize(text, font=text_font)
        draw.text((int((card_width-text_width)/2), image_margin*1.5 + image_dimensions[0]), text, text_color, font=text_font)

        bytes_io = BytesIO()
        img.save(bytes_io, "PNG")
        return bytes_io

    def generate_PNG(self, dictionary, join=False):
        """
{'cards': [{'gramm': 'DET', 'image_path': ['el.png'], 'text': 'El'}, {'gramm': 'SUST', 'image_path': ['niño.png', 'niño_3.png', 'niño_1.png', 'niño_2.png'], 'text': 'niño'}, {'gramm': 'SUST', 'image_path': ['comer.png', 'comer_2.png', 'comer_1.png', 'comer_5.png', 'comer_4.png', 'comer_3.png'], 'text': 'come'}, {
        'gramm': 'SUST', 'image_path': ['pan_1.png', 'pan_2.png', 'pan.png'], 'text': 'pan'}], 'colors': {'SUST': '#d32f2f', 'ADJ': '#2e7d32', 'DET': '#1565c0', 'PRON': '#d32f2f', 'VERB': '#ff6f00', 'ADVERB': '#004d40', 'INTERJ': '#37474f', 'PREP': '#c2185b', 'CONJ': '#c2185b', 'OTHER': '#eeeeee'}, 'type': 'color', 'images': [0, 0, 0, 2]}

        """
        
        pass
        """
        cards = dictionary['cards']
        colors = dictionary['colors']
        type = dictionary['type']
        images = dictionary['images']

        length = len(cards)
        _, cards_height = self.__card_dimensions

        if join:
            cards_width = self.__image_margin + (self.__card_dimensions[0] - self.__image_margin)*length
            cards_repeat = self.__card_dimensions[0] - self.__image_margin
        else:
            cards_width = self.__card_dimensions[0]*length
            cards_repeat = self.__card_dimensions
        
        imgs = []
        i = 0
        for card in cards:
            imgs.append(self.generate_card2(card['text'], colors[card['gramm']], card['image_path'][images[i]]))
            i += 1
        
        i = 0
        for img in imgs:
            img.seek(0)
            bytes = img.read()
            data = BytesIO(bytes)
            card_img = Image.open(data)#frombytes('RGB', self.__card_dimensions, img.getvalue(), 'raw')
            img.paste(card_img, (i*cards_repeat, 0))
            i += 1
        
        bytes_io = BytesIO()
        img.save(bytes_io, "PNG")
        
        return bytes_io
        """

    def generate_ZIP(self, dictionary):
        cards = dictionary['cards']
        colors = dictionary['colors']
        type = dictionary['type']
        images = dictionary['images']

        beginning = "pictomaker-"
        files = []
        i = 0
        for card in cards:
            filename = beginning+str(i)+"_"+card['text']+".png"
            io = BytesIO()
            io = self.generate_card2(card['text'], colors[card['gramm']], self.__base_path+type+"/"+card['image_path'][images[i]])
            data = io.getvalue()
            io.close()
            files.append((filename, data))

            """ print(card['text'])
            print(colors[card['gramm']])
            print("./static/"+type+"/"+card['image_path'][images[i]])
            img = self.generate_card2(card['text'], colors[card['gramm']], "./static/"+type+"/"+card['image_path'][images[i]])
            filename = "./generating/"+beginning+str(i)+"_"+card['text']+".png"
            PictoImageHandler.write_bytesio_to_file(filename, img)
            filenames.append(filename)
            print("written to "+filename) """
            i += 1
        
        mem_io = BytesIO()

        with zipfile.ZipFile(mem_io, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                zf.writestr(f[0], f[1])

        #for file in filenames:
        #    os.remove(file)
        
        return mem_io

    @staticmethod
    def write_bytesio_to_file(filename, bytesio):
        """
        Write the contents of the given BytesIO to a file.
        Creates the file or overwrites the file if it does
        not exist yet. 
        """
        with open(filename, "wb") as outfile:
            # Copy the BytesIO stream to the output file
            outfile.write(bytesio.getbuffer())