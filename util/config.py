import json

with open("config/config.json") as config:
    settings = json.load(config)


def books():
    return settings["urls"]


def book(key):
    return settings["urls"][key]


def mail(key=None):
    if key is None:
        return settings["mail"]
    return settings["mail"][key]


def server_chan():
    return settings["serverChan"]["scKey"]
