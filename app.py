#!/usr/bin/env python
from __future__ import print_function
from flask import Flask, render_template, make_response
from flask import redirect, request, jsonify, url_for

from imagehandler import PictoImageHandler
from interface import PictoInterface
from language import PictoLanguage

import io
import os
import uuid
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.debug = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/editor', methods=['GET'])
def editor():
    return render_template('editor.html')

@app.route('/results/<uuid>', methods=['GET'])
def results(uuid):
    title = 'Result'
    data = get_file_content(uuid)
    return render_template('layouts/results.html',
                           title=title,
                           data=data)

@app.route('/textpost', methods = ['POST'])
def post_text():
    text = request.form['text']
    cards = interface.get_cards(text)
    cards_json = []
    for c in cards:
        print(c.to_json())
        cards_json.append(c.to_json())
    
    return jsonify({'cards': cards_json})
    #return jsonify({'message': "OK"})

@app.route('/postmethod', methods = ['POST'])
def post_javascript_data():
    jsdata = request.form['canvas_data']
    unique_id = create_csv(jsdata)
    params = { 'uuid' : unique_id }
    return jsonify(params)

@app.route('/plot/<imgdata>')
def plot(imgdata):
    data = [float(i) for i in imgdata.strip('[]').split(',')]
    data = np.reshape(data, (200, 200))
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.axis('off')
    axis.imshow(data, interpolation='nearest')
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

def create_csv(text):
    unique_id = str(uuid.uuid4())
    with open('images/'+unique_id+'.csv', 'a') as file:
        file.write(text[1:-1]+"\n")
    return unique_id

def get_file_content(uuid):
    with open('images/'+uuid+'.csv', 'r') as file:
        return file.read()

if __name__ == '__main__':
    image_handler = PictoImageHandler(
        font = "./resources/escolar_bold.ttf",
        text_size = 90,
        card_dimensions = (600,750),
        image_margin = 50
    )
    print("Starting language toolkit...")
    language = PictoLanguage()
    print("Language toolkit started")
    interface = PictoInterface(language, image_handler)
    app.run(host='0.0.0.0', port=5000)
