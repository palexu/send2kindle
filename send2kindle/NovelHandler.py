# 主处理器，分配对应的处理器给页面
def get_novel_handler(domain):
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

    def get_novel_name_chi(self, index_page):
        return index_page.find("div", {"id": "info"}).h1.get_text()

    def get_novel_name_en(self, page):
        return "en_name"

    def chapter_filter(self, list):
        return list[12:]


if __name__ == '__main__':
    get_novel_handler("www.biqudao.com")
