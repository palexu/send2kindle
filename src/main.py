# coding=utf-8
import yaml
import Novel

if __name__ == '__main__':
    # 默认发送每三章节发送一次
    # 0，1：一有新章节就发送
    # 2-n：累积n章节后发送
    with open("config/config.yaml") as config:
        settings = yaml.load(config)
        print(settings)
    service = Novel.Service()
    service.load_config(settings)
    service.all_novels_latest_updates_2_kindle()
