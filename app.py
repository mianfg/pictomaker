#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask app
=========

This module runs the Flask app.

"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2019, Bloomgogo"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "GPL"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "mianfg@bloomgogo.com"
__status__      = "Production"


# Flask imports
from flask import Flask, render_template, make_response, send_file
from flask import redirect, request, jsonify, url_for

# Python libary imports
from io import BytesIO
import json, uuid, os, time

# PictoMaker imports
from imagehandler import PictoImageHandler
from interface import PictoInterface
from language import PictoLanguage
from card import PictoCard


app = Flask(__name__)
app.secret_key = 's3cr3t'
app.debug = True

# global
image_handler = None
language = None
interface = None


@app.before_first_request
def start():
    """
    Starts the app
    """
    global image_handler
    global language
    global interface
    image_handler = PictoImageHandler(
        font="./static/fonts/escolar_bold.ttf",
        text_size=90,
        card_dimensions=(600, 750),
        image_margin=50,
        base_path="https://raw.githubusercontent.com/mianfg/pictomaker/master/static/"
    )
    print("Starting language toolkit...")
    language = PictoLanguage()
    print("Language toolkit started")
    interface = PictoInterface(language, image_handler)


@app.route('/', methods=['GET'])
def index():
    """
    Renders HTML
    """
    return render_template('index.html')


@app.route('/test_download', methods=['GET', 'POST'])
def test_download():
    """
    Test function
    WIP: delete
    """
    print("Entered this place --WIP--")
    # Use BytesIO instead of StringIO here.
    buffer = BytesIO()
    buffer.write(b'jJust some letters.')
    # Or you can encode it to bytes.
    # buffer.write('Just some letters.'.encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True,
                     attachment_filename='a_file.txt',
                     mimetype='text/csv')


@app.route('/textpost', methods=['POST'])
def post_text():
    """
    Receives sentence for PictoMaker to translate, returns cards
    """
    global interface
    text = request.form['text']
    cards = interface.get_cards(text)
    cards_json = []
    for c in cards:
        print(c.to_dict())
        cards_json.append(c.to_dict())

    return jsonify({'cards': cards_json})


@app.route('/imagesearch', methods=['POST'])
def post_imagesearch():
    """
    Receives image search request, sends search results
    """
    global interface
    text = request.form['text']
    results = interface.get_literal(text)

    return jsonify({'results': results})


@app.route('/generate/pdf', methods=['POST'])
def get_pdf():
    """
    Receives card data, returns PDF file
    """
    global image_handler
    values = request.form['values']
    values = json.loads(values)

    print(values)
    """
    cards = values['cards']
    colors = values['colors']
    type = values['type']
    images = values['images']

    io = image_handler.generate_PDF(cards, colors, type, images)
    
    return send_file(
        io,
        as_attachment=True,
        attachment_filename="pictomaker_"+uuid.uuid1(),
        mimetype='application/pdf'
    )
    """


@app.route('/generate/png', methods=['POST'])
def get_png():
    """
    Receives card data, returns PNG file
    """
    global image_handler
    if request.method == "POST":
        values = request.form['values']
        values = json.loads(values)

        cards = values['cards']
        colors = values['colors']
        type = values['type']
        images = values['images']

        io = image_handler.generate_PNG(values)
        filename = "pictomaker_"+str(uuid.uuid1())+".png"
        url = "/static/generate/" + filename
        image_handler.write_bytesio_to_file("."+url, io)
        return jsonify({'url': url, 'filename': filename})
    """io.seek(0)

    return send_file(
        io,
        as_attachment=True,
        attachment_filename="pictomaker_"+str(uuid.uuid1())+".png",
        mimetype='image/png'
    )
    """

@app.route('/generate/zip', methods=['POST'])
def get_zip():
    """
    Receives card data, returns ZIP file
    """
    global image_handler
    if request.method == "POST":
        values = request.form['values']
        values = json.loads(values)

        io = image_handler.generate_ZIP(values)
        filename = "pictomaker_"+str(uuid.uuid1())+".zip"
        url = "/static/generate/" + filename
        image_handler.write_bytesio_to_file("."+url, io)
        return jsonify({'url': url, 'filename': filename})

@app.route('/generate/delete', methods=['POST'])
def got_png():
    """
    Deletes temp PNG file
    """
    values = request.form['values']
    values = json.loads(values)

    url = values['url']
    time.sleep(3)
    os.remove("."+url)

    return jsonify({'url': url})


if __name__ == '__main__':
    """
    Main function
    """
    # run app
    app.run(host='0.0.0.0', port=5000)
