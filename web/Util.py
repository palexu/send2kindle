import json


def class2json(clazz):
    return json.dumps(clazz, default=lambda obj: obj.__dict__)
