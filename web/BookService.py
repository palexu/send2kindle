from flask import Flask, render_template
from flask import request

from sender.novel.model import BookConfig
from util.config import books
from . import app


@app.route('/book/update/<book_name>')
def update(book_name):

    return render_template("/book/update/form.html")
