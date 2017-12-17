from flask import Flask, render_template
from sender.novel.model import BookConfig
from util.config import books
from . import app

@app.route('/')
def index():
    bcs = []
    for b in books():
        bc = BookConfig(b)
        bcs.append(bc)
    return render_template('index.html', book_configs=bcs)

