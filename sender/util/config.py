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

def load_config():
    with open(confg_path) as f:
        return json.load(f)


def mail():
    return load_config()["mail"]


def server_chan():
    try:
        return load_config()["serverChan"]["scKey"]
    except:
        return ""


def write_mail(mail_config):
    settings = load_config()
    with open(confg_path, "w") as f:
        settings["mail"] = mail_config
        j = json.dumps(settings)
        f.write(j)


def write_server_chan(sc_config):
    settings = load_config()
    with open(confg_path, "w") as f:
        settings["serverChan"] = sc_config
        j = json.dumps(settings)
        f.write(j)
