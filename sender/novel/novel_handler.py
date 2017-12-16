# coding=utf-8


def dispacher(domain):
    """主处理器，分配对应的处理器给页面"""
    handler = []
    # 添加handler到列表中
    biqugeHandler = BiqugeHandler()
    handler.append(biqugeHandler)

    for h in handler:
        if h.handler_name == domain:
            return h


# 一个处理器对应一个网站的网页格式
class BiqugeHandler:
    def __init__(self):
        # 该处理器的唯一标志符号
        self.handler_name = "www.biqudao.com"

    @staticmethod
    def get_base_url():
        return "http://www.biqudao.com"

    def chapter_filter(self, list):
        return list[12:]
