<p align="center">
    <img src="./static/img/logos/logo-dark.png" width="500px">
</p>

<h1 align="center"><p align="center">PictoMaker</h1></h1>

> Created by **Miguel Ángel Fernández Gutiérrez** · https://mianfg.bloomgogo.com/

## Introduction

**PictoMaker** is a web app that translates texts into sequences of pictograms.

> NOTE: as of the latest update, PictoMaker only supports Spanish.

## Run locally

To locally run the app, you must run the following commands:

```bash
pip install -r requirements.txt
python -m spacy download es_core_news_md
```

Then type the following command to run the app in a development Flask server, on `0.0.0.0:5000`:

```bash
python app.py
```