<p align="center">
    <img src="./static/img/logos/logo-dark.png" width="500px">
</p>

<h1 align="center"><p align="center">PictoMaker</h1></h1>

> Created by **Miguel Ángel Fernández Gutiérrez** · https://mianfg.bloomgogo.com/
> **Try this app out at <https://pictomaker.herokuapp.com/>!**

## Introduction

**PictoMaker** is a web app that translates texts into sequences of pictograms.

## Important notice

> This app is **under development**, and the scripts provided **lack documentation**. Some of the code may be written in a not-so-pretty way, but do not worry -- I am working to tidy all this up as soon as possible!
>
> The documentation will be presumably finished once all the features that are on my waitlist are implemented. Thanks for the patience! :happy:

## Features

PictoMaker includes the following features:

* **Sytactical analysis** using a natural language toolkit (`nltk`).

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
