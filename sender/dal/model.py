# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from peewee import *



class Book:
    """小说"""

    def __init__(self, book_name):
        self.book_name = book_name
        self.sections = []

    def add_section(self, chapter_name, chapter_content):
        self.sections.append((chapter_name, chapter_content))

