from flask import Flask
import os
app = Flask(__name__)
# path = os.path.dirname(os.path.abspath("static"))+"/static"
# print(path)
# app._static_folder = path



from . import ConfigService
from . import BookService