# coding=utf-8
from __future__ import unicode_literals

import logging

from collections import OrderedDict
from lib.calibre.ebooks.conversion.mobioutput import MOBIOutput
from lib.calibre.ebooks.conversion.epuboutput import EPUBOutput
from lib.calibre.utils.bytestringio import byteStringIO
from lib.makeoeb import *

log = logging.getLogger()

opts = None
oeb = None

opts = getOpts()
oeb = CreateOeb(log, None, opts)
setMetaData(oeb, title="heello")

GENERATE_HTML_TOC = True
GENERATE_TOC_THUMBNAIL = True

insertHtmlToc = GENERATE_HTML_TOC
insertThumbnail = GENERATE_TOC_THUMBNAIL

sections = OrderedDict()
sections.setdefault("科幻", [])
sections["科幻"].append(("神级学霸", "b", "c",
                       "<body>学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸学霸</body>"))
sections["科幻"].append(("小说2", "b", "c", "<body>的滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答的</body>"))
sections.setdefault("科技", [])
sections["科技"].append(
    ("未来的人", "b", "c", "<body>未来的人未来的人未来的人未来的人未来的人未来的人未来的人未来的人未来的人未来的人未来的人未来的人未来的人未来的人未来的人未来的人未来的人未来的人</body>"))
sections["科技"].append(("未来的人", "b", "c", "<body>的滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答滴滴答答的</body>"))
toc_thumbnails = {"c": "https://www.google.com.hk/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"}

InsertToc(oeb, sections, toc_thumbnails, insertHtmlToc, insertThumbnail)

oIO = byteStringIO()
o = MOBIOutput()

o.convert(oeb, oIO, opts, log)

print(oIO)
with open("bbb.mobi", "wb+") as f:
    f.write(oIO.getvalue())
