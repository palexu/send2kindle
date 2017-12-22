from flask import Flask

app = Flask(__name__)

from . import ConfigService
from . import BookService
from . import SenderService
from . import IndexService
