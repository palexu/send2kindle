# coding=utf8
import requests


def send(scKey,title, message):
    url = "https://sc.ftqq.com/" + scKey + ".send?text=" + title + "&desp=" + message
    requests.get(url)


if __name__ == '__main__':
    send('hehe', 'messssssss')
