import json

with open("config/config.json") as config:
    settings = json.load(config)


def url(key):
    return settings["urls"][key]


def mail(key=None):
    if key is None:
        return settings["mail"]
    return settings["mail"][key]


def server_chan():
    return settings["server_chan"]["scKey"]
