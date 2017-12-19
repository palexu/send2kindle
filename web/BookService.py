# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import jsonify, request
from .Util import class2json
import json

from sender.dal.service import BookService
from . import app


class BookApi:

    def __init__(self):
        self.service = BookService()

    @app.route('/api/book/add', methods=['POST'])
    def insert(self):
        """
        book={
             "key":value,
        }
        :return:
        """
        book = request.get_json()
        self.service.add_book(book)
        return ""

    @app.route('/api/book/update', methods=['POST'])
    def update(self):
        """
        book = {
            "key":value,
        }
        :return:
        """
        book = request.get_json()
        self.service.update_by_id(book)
        return ""

    @app.route('/api/book/delete/<id>')
    def delete(self, id):
        """
        书籍的初始化
        :return:
        """
        self.service.delete_by_id(id)
        return jsonify({
            "isSuccess": True
        })

    @app.route('/api/book/all')
    def all(self, ):
        books = self.service.select_all()
        return jsonify(class2json(books))
