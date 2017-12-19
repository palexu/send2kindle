from flask import Flask, Response, jsonify

#
#
# class MyResponse(Response):
#     @classmethod
#     def force_type(cls, response, environ=None):
#         if isinstance(response, (list, dict)):
#             response = jsonify(response)
#         else
#             response =
#         return super(Response, cls).force_type(response, environ)


app = Flask(__name__)
# app.response_class = MyResponse

from . import ConfigService
from . import BookService
from . import SenderService
from . import InitService
