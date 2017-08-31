# coding=utf-8
import yaml
from send2kindle import Novel

if __name__ == '__main__':
    with open("../config/config.yaml") as config:
        settings = yaml.load(config)
    print(settings)
    service = Novel.Service(settings)
    service.all_novels_latest_updates_2_kindle()
