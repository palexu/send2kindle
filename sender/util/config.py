import json
import logging.config

# ======================  db ============================
db_path = "db/novel.db"
confg_path = "config.json"

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
with open(confg_path) as f:
    settings = json.load(f)


def mail():
    return settings["mail"]


def server_chan():
    try:
        return settings["serverChan"]["scKey"]
    except:
        return ""
