# coding=utf-8
from __future__ import unicode_literals

from collections import OrderedDict
from calibre.ebooks.conversion.mobioutput import MOBIOutput
from calibre.ebooks.conversion.epuboutput import EPUBOutput
from calibre.utils.bytestringio import byteStringIO
from util.makeoeb import *
from util.config import *


class Ebook:
    def __init__(self, ebook_name):
        self.opts = getOpts()
        self.oeb = CreateOeb(logger, None, self.opts)
        self.ebook_name = ebook_name

        # 防止发出无内容的空书
        self.has_content = False

        setMetaData(self.oeb, title=ebook_name)

        GENERATE_HTML_TOC = True
        GENERATE_TOC_THUMBNAIL = True

        self.insertHtmlToc = GENERATE_HTML_TOC
        self.insertThumbnail = GENERATE_TOC_THUMBNAIL

        self.sections = OrderedDict()
        self.book = MOBIOutput()

    def as_epub(self):
        self.book = EPUBOutput()
        return self

    def as_mobi(self):
        self.book = MOBIOutput()
        return self

    def add_section(self, book_name, chapter, content):
        self.sections.setdefault(book_name, [])
        self.sections[book_name].append((chapter, "b", "c", "<body>" + content + "</body>"))
        return self

    def add_sections(self, bookname, sections):
        if not sections:
            return

        try:
            for title, content in sections:
                self.add_section(bookname, title, content)
        except Exception as e:
            print(e)

        self.has_content = True

    def get_byte_book(self):
        if not self.has_content:
            return None

        toc_thumbnails = {"c": "https://www.google.com.hk/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"}

        InsertToc(self.oeb, self.sections, toc_thumbnails, self.insertHtmlToc, self.insertThumbnail)

        byte_book = byteStringIO()

        self.book.convert(self.oeb, byte_book, self.opts, logger)

        return byte_book.getvalue()
