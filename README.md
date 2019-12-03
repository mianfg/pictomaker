<p align="center">
    <img src="./static/img/logos/logo-dark.png" width="500px">
</p>

<h1 align="center"><p align="center">PictoMaker</h1></h1>

> Created by **Miguel Ángel Fernández Gutiérrez** · https://mianfg.bloomgogo.com/

## Introduction

**PictoMaker** is a web app that translates texts into sequences of pictograms.

## Features

PictoMaker includes the following features:

* **Sytactical analysis** using a natural language toolkit (`nltk`).
* **Syntax highlighting**, coloring the borders of each card depending on the category of the word.
* **Custom highlighting styles**: the border color can be changed.
* **Colored/uncolored pictograms**: can switch between colored pictograms and black and white pictograms.
* **File export:** cards can be exported to:
  * PNG: single image with the entire sentence.
  * ZIP: individual cards, as PNG, compressed.
  * PDF: for printing.

And much more! You can test it at <https://pictomaker.heroku.com/>

> **Important notice:** as of the most recent update, PictoMaker only supports Spanish.

## Run locally

To locally run the app, you must execute the following commands:

```bash
pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

Then type the following command to run the app in a development Flask server, on `0.0.0.0:5000`:

```bash
python app.py
```