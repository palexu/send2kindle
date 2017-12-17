import json
import logging.config

# ======================  db ============================
db = "db/novel.db"

# ====================log config ========================
logging_config = dict(
    version=1,
    formatters={
        'f': {'format':
                  '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
    },
    root={
        'handlers': ['h'],
        'level': logging.INFO,
    },
)
logging.config.dictConfig(logging_config)
logger = logging.getLogger()

# =====================book config========================
with open("config.json") as f:
    settings = json.load(f)


def books():
    return settings["books"]


def book(key):
    return settings["urls"][key]


def mail():
    return settings["mail"]


def server_chan():
    try:
        return settings["serverChan"]["scKey"]
    except:
        return ""
