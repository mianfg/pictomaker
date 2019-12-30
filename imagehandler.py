#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PictoImageHandler
=================

This module generates images and files from card data
"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2019, Bloomgogo"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "GPL"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "mianfg@bloomgogo.com"
__status__      = "Production"


# Python library imports
from PIL import Image, ImageOps, ImageDraw, ImageFont
#import fpdf
from io import BytesIO
import urllib.request, requests, uuid, zipfile, os

# PictoMaker imports
from manager import PictoManager
from language import PictoLanguage


class PictoImageHandler:
    """
    Class used to generate images and files from card data

    ...

    Attributes
    ----------
    __font : str
        Absolute path to font file (ttf)
    __text_size : int
        Text size, in pt
    __card_dimensions : (int, int)
        Card dimensions, in px; (width, height)
    __image_margin : int
        Image margin, in px
    __base_path :
        Base path to images (must be static path)

    Methods
    -------
    get_URL(path, type)
        Gets absolute path, from URL or locally
    generate_card(card)
        Generates single card, in PNG format
    generate_PNG(card)
        Generates image with multiple cards, in PNG format

    """
    def __init__(self, font, text_size, card_dimensions, image_margin, base_path):
        self.__font = font
        self.__text_size = text_size
        self.__card_dimensions = card_dimensions
        self.__image_margin = image_margin
        self.__base_path = base_path

    def get_URL(self, path, type):
        if type == "URL":
            return path
        else:
            return self.__base_path+type+"/"+path

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

    def generate_card(self, text, color, image_url):
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
        
        picto = ImageOps.fit(picto, image_dimensions, centering=(0.5,0.5)) #WIP check
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
            cards_repeat = self.__card_dimensions[0]
        
        full = Image.new('RGB', (cards_width, cards_height), (255,255,255))

        i = 0
        for card in cards:
            img = self.generate_card(card['text'], colors[card['gramm']], self.get_URL(card['image_path'][images[i]], type))
            #img.seek(0)
            card_img = Image.open(img)
            full.paste(card_img, (i*cards_repeat, 0))
            i += 1
        
        bytes_io = BytesIO()
        full.save(bytes_io, "PNG")
        
        return bytes_io
        

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
            io = self.generate_card(card['text'], colors[card['gramm']], self.get_URL(card['image_path'][images[i]], type))
            data = io.getvalue()
            io.close()
            files.append((filename, data))

            """ print(card['text'])
            print(colors[card['gramm']])
            print("./static/"+type+"/"+card['image_path'][images[i]])
            img = self.generate_card(card['text'], colors[card['gramm']], "./static/"+type+"/"+card['image_path'][images[i]])
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

    def generate_PDF(self, dictionary, output_file):
        pass
        """
        cards = dictionary['cards']
        colors = dictionary['colors']
        type = dictionary['type']
        images = dictionary['images']

        pdf = fpdf.FPDF()
        #pdf.compress = false

        i = 0
        for card in cards:
            pdf.add_page()
            img = self.generate_card(card['text'], colors[card['gramm']], self.get_URL(card['image_path'][images[i]], type))
            pdf.image('arbitrarynameofimage', x=0, y=0, w=self.__card_dimensions[0],\
                h=self.__card_dimensions[1], type='png', link=None, file=img)
            i += 1
        
        pdf.output(output_file, 'F')
        """
    

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

"""test
imag= PictoImageHandler(
    font = "./static/fonts/escolar_bold.ttf",
    text_size = 90,
    card_dimensions = (600,750),
    image_margin = 50,
    base_path = "https://raw.githubusercontent.com/mianfg/pictomaker/master/static/"
)
dictionary = {'cards': [{'gramm': 'DET', 'image_path': ['el.png'], 'text': 'El'}, {'gramm': 'ADJ', 'image_path': ['pequeño.png'], 'text': 'pequeño'}, {'gramm': 'SUST', 'image_path': ['niño.png', 'niño_1.png', 'niño_2.png', 'niño_3.png'], 'text': 'Miguel Ángel'}, {'gramm': 'VERB', 'image_path': ['querer.png', 'querer_1.png', 'querer_2.png', 'querer_3.png', 'querer_4.png', 'querer_5.png', 'querer_6.png', 'querer_7.png', 'querer_8.png', 'querer_9.png'], 'text': 'quiere'}, {'gramm': 'VERB', 'image_path': ['ir.png', 'ir_1.png', 'ir_2.png', 'ir_3.png', 'ir_4.png', 'ir_5.png'], 'text': 'ir'}, {'gramm': 'PREP', 'image_path': ['A_1.png', 'a.png', 'a_2.png'], 'text': 'a'}, {'gramm': 'DET', 'image_path': ['su.png', 'su_1.png'], 'text': 'su'}, {'gramm': 'SUST', 'image_path': ['casar.png', 'casa.png'], 'text': 'casa.'}], 'colors': {'SUST': '#d32f2f', 'ADJ': '#2e7d32', 'DET': '#1565c0', 'PRON': '#d32f2f', 'VERB': '#ff6f00', 'ADVERB': '#004d40', 'INTERJ': '#37474f', 'PREP': '#c2185b', 'CONJ': '#c2185b', 'OTHER': '#eeeeee'}, 'type': 'color', 'images': [0, 0, 3, 7, 0, 2, 0, 1]}

io = imag.generate_PNG(dictionary)
PictoImageHandler.write_bytesio_to_file("./static/img/tutorial/example.png", io)
"""