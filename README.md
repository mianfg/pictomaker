<p align="center">
    <img src="./static/img/logos/logo-dark.png" width="500px">
</p>

<h1 align="center">PictoMaker (deprecated)</h1>
<p align="center" id="badges">
    <a href="https://github.com/mianfg/pictomaker/blob/master/LICENSE"><img src="https://img.shields.io/github/license/mianfg/pictomaker" alt="License"></a> <a href="#"><img src="https://img.shields.io/github/languages/code-size/mianfg/pictomaker" alt="Code size"></a> <a href="https://github.com/mianfg/pictomaker/commits"><img src="https://img.shields.io/github/last-commit/mianfg/pictomaker" alt="Last commit"></a> <a href="#"><img src="https://img.shields.io/badge/status-deprecated-red" alt="More info"></a> <a href="https://go.mianfg.me/pictomaker"><img src="https://img.shields.io/badge/-more%20info-orange" alt="More info"></a>
</p>

> Created by **Miguel Ángel Fernández Gutiérrez** · <https://mianfg.me/> 
> 
> **Try this app out at <https://pictomaker.mianfg.me/>!**

## Introduction

**PictoMaker** is a web app that translates sentences into sequences of pictograms.

## ⚠️ Important notice

> This version of PictoMaker is **deprecated**. You can enjoy a **new, more elegant and improved version** called [PictoMaker Lite](https://github.com/mianfg/pictomaker-lite). PictoMaker Lite is a low overhead API designed to provide basic functionality, and with more features!
> 
> * Better tokenization and lemmatization.
> * More organized code.
> * Multilanguage support!
> 
> _The scripts provided here **lack documentation**, and some of the code may be written in a not-so-pretty way (as this was the first webapp that I ever implemented 😅). Please do not use in production. This repository has been left as-is, as I'm frankly really proud of it!_

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
