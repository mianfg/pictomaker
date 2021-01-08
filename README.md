<p align="center">
    <img src="./static/img/logos/logo-dark.png" width="500px">
</p>

<h1 align="center"><p align="center">PictoMaker</h1></h1>

> Created by **Miguel Ángel Fernández Gutiérrez** · <https://mianfg.me/> 
> 
> **Try this app out at <https://pictomaker.herokuapp.com/>!**

## Introduction

**PictoMaker** is a web app that translates sentences into sequences of pictograms.

## ⚠️ Important notice

> This version of PictoMaker is **deprecated**. I am working on a new, faster and more efficient (and with more elegant code) version with more features. On the meantime, you can enjoy this app at <https://pictomaker.herokuapp.com/>.
> 
> The scripts provided **lack documentation**, and some of the code may be written in a not-so-pretty way (as this was the first webapp that I ever implemented 😅). Please do not use in production. Soon there will be a new version, as I previosly stated.

## Features

PictoMaker includes the following features:

* **Sytactical analysis** using a natural language processing toolkit (`nltk`).

* **Syntax highlighting**, coloring the borders of each card depending on the category of the word.

* **Custom highlighting styles**: the border color can be changed.

* **Colored/uncolored pictograms**: can switch between colored pictograms and black and white pictograms.

* **Pictogram search engine**: you can change the photos using our search engine, or you can add your **custom ones** via URL.

  > **Upcoming:** Custom photo by URL is under development.

* **File export:** cards can be exported to:
  
  * PNG: single image with the entire sentence.
  
  * ZIP: individual cards, as PNG, compressed.
  
  * PDF: for printing.
  
    > **Upcoming:** PDF output is under development.

And much more! You can test it out at <https://pictomaker.herokuapp.com/>

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
