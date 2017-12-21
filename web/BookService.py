# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import jsonify, request
from sender.util.config import logger
from sender.dal.service import BookService
from . import app


@app.route('/api/book/add', methods=['POST'])
def insert():
    """
    book={
         "key":value,
    }
    :return:
    """
    book = request.get_json()
    print(book)
    BookService().add_book(book)
    return ""


@app.route('/api/book/update/<id>', methods=['POST'])
def update(id):
    """
    book = {
        "key":value,
    }
    :return:
    """
    book = request.get_json()
    BookService().update_by_id(id, book)
    return ""


@app.route('/api/book/delete/<id>')
def delete(id):
    BookService().delete_by_id(id)
    return jsonify({
        "isSuccess": True
    })


@app.route('/api/book/all')
def all():
    books = BookService().select_all()
    ds = []
    for b in books:
        ds.append(b.to_dict())
    return jsonify(ds)
