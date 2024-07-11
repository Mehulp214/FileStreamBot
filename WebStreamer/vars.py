# This file is a part of FileStreamBot

from os import environ
from dotenv import load_dotenv

load_dotenv()


class Var(object):
    MULTI_CLIENT = True
    API_ID = int(environ.get("API_ID", 13216322))
    API_HASH = str(environ.get("API_HASH", "15e5e632a8a0e52251ac8c3ccbe462c7"))
    BOT_TOKEN = str(environ.get("BOT_TOKEN", "7084473050:AAEra4gISnQVGHdFka6BHx71PJvj9E8w0gY"))
    SLEEP_THRESHOLD = int(environ.get("SLEEP_THRESHOLD", "60"))  # 1 minte
    WORKERS = int(environ.get("WORKERS", "6"))  # 6 workers = 6 commands at once
    #BIN_CHANNEL = int(
    #    environ.get("BIN_CHANNEL", None))
    BIN_CHANNEL=-1002175816545
    # you NEED to use a CHANNEL when you're using MULTI_CLIENT
    PORT = int(environ.get("PORT", 2400))
    
    BIND_ADDRESS = str(environ.get("WEB_SERVER_BIND_ADDRESS", "109.199.117.175"))
    PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
    HAS_SSL = str(environ.get("HAS_SSL", "0").lower()) in ("1", "true", "t", "yes", "y")
    NO_PORT = str(environ.get("NO_PORT", "0").lower()) in ("1", "true", "t", "yes", "y")
    FQDN = str(environ.get("FQDN", BIND_ADDRESS))
    URL = "http{}://{}{}/".format(
            "s" if HAS_SSL else "", FQDN, "" if NO_PORT else ":" + str(PORT)
        )

    DATABASE_URL = str(environ.get('DATABASE_URL', "mongodb+srv://newuser_31:qwerty_1234@cluster0.lajjdmy.mongodb.net/"))
    UPDATES_CHANNEL = str(environ.get('UPDATES_CHANNEL', "mehulbots"))
    OWNER_ID = int(environ.get('OWNER_ID', '5993556795'))
    SESSION_NAME = str(environ.get('SESSION_NAME', 'F2LxBot'))
    FORCE_UPDATES_CHANNEL = environ.get('FORCE_UPDATES_CHANNEL', False)
    FORCE_UPDATES_CHANNEL = True if str(FORCE_UPDATES_CHANNEL).lower() == "true" and UPDATES_CHANNEL != 'aredirect' else False

    BANNED_CHANNELS = list(set(int(x) for x in str(environ.get("BANNED_CHANNELS", "-1001296894100")).split()))
    KEEP_ALIVE = str(environ.get("KEEP_ALIVE", "0").lower()) in  ("1", "true", "t", "yes", "y")
