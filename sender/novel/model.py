# coding=utf-8


class Book:
    """小说"""

    def __init__(self, bookname):
        self.book_name = bookname
        self.sections = []

    def add_section(self, chapter_name, chapter_content):
        self.sections.append((chapter_name, chapter_content))
