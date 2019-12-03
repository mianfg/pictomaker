#!/usr/bin/env python
from __future__ import print_function
from flask import Flask, render_template, make_response, send_file
from flask import redirect, request, jsonify, url_for
import json, uuid

from imagehandler import PictoImageHandler
from interface import PictoInterface
from language import PictoLanguage
from card import PictoCard


app = Flask(__name__)
app.secret_key = 's3cr3t'
app.debug = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/textpost', methods = ['POST'])
def post_text():
    text = request.form['text']
    cards = interface.get_cards(text)
    cards_json = []
    for c in cards:
        print(c.to_dict())
        cards_json.append(c.to_dict())
    
    return jsonify({'cards': cards_json})


@app.route('/generate/pdf', methods = ['POST'])
def get_pdf():
    values = request.form['values']
    values = json.loads(values)

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

@app.route('/generate/png', methods = ['POST'])
def get_png():
    values = request.form['values']
    values = json.loads(values)

    cards = values['cards']
    colors = values['colors']
    type = values['type']
    images = values['images']

    io = image_handler.generate_PNG(cards, colors, type, images)
    
    return send_file(
        io,
        as_attachment=True,
        attachment_filename="pictomaker_"+uuid.uuid1(),
        mimetype='image/png'
    )


@app.route('/generate/zip', methods = ['POST'])
def get_zip():
    values = request.form['values']
    values = json.loads(values)

    io = image_handler.generate_ZIP(values)

    return send_file(
        io,
        attachment_filename="pictomaker_"+str(uuid.uuid1())+".zip",
        mimetype='application/zip',
        as_attachment=True
    )


if __name__ == '__main__':
    image_handler = PictoImageHandler(
        font = "./static/fonts/escolar_bold.ttf",
        text_size = 90,
        card_dimensions = (600,750),
        image_margin = 50,
        base_path = "https://raw.githubusercontent.com/mianfg/pictomaker/master/static/"
    )

    print("Starting language toolkit...")
    language = PictoLanguage()
    print("Language toolkit started")
    interface = PictoInterface(language, image_handler)
    app.run(host='0.0.0.0', port=5000)
