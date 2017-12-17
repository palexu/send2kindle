# coding=utf8
import requests
import util.config as config


def send(title, message=None):
    scKey = config.server_chan()
    if not scKey:
        return

    if message:
        url = "https://sc.ftqq.com/" + scKey + ".send?text=" + title + "&desp=" + message
    else:
        url = "https://sc.ftqq.com/" + scKey + ".send?text=" + title
    requests.get(url)
