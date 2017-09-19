# coding=utf-8
import yaml
import sys

sys.path.append("../")
from send2kindle import Novel


def run():
    with open("../config/config.yaml") as config:
        settings = yaml.load(config)
    print(settings)
    service = Novel.Service(settings)
    service.all_novels_latest_updates_2_kindle()

if __name__ == '__main__':
    run()
