# coding=utf-8


class Book:
    """小说"""

    def __init__(self):
        self.book_name = ""
        self.sections = []

    def add_section(self, chapter_name, chapter_content):
        self.sections.append((chapter_name, chapter_content))
