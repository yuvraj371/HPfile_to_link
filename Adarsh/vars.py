import os
from os import getenv, environ
from dotenv import load_dotenv

load_dotenv()

class Var(object):
    # Basic settings
    MULTI_CLIENT = False
    API_ID = int(getenv('21938068'))  # Your API ID
    API_HASH = str(getenv('c18fd98f3e58484df0aecd95a3d5a6a9'))  # Your API Hash
    BOT_TOKEN = str(getenv('5972634422:AAG2Q7ozpB4tKCVTCTJcFT7504GpeUYNTgM'))  # Your bot token
    name = str(getenv('SESSION_NAME', 'filetolinkbot'))
    SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
    WORKERS = int(getenv('WORKERS', '4'))

    # Telegram configuration
    BIN_CHANNEL = int(getenv('-1001730461072'))  # Your Bin Channel
    OWNER_ID = set(int(x) for x in os.environ.get("OWNER_ID", "5787509903").split())  # List of owner IDs
    OWNER_USERNAME = str(getenv('Madhuri_niranjan'))  # Owner's username

    # Network settings
    NO_PORT = bool(getenv('NO_PORT', False))
    APP_NAME = None

    # Heroku configuration
    if 'DYNO' in environ:
        ON_HEROKU = True
        APP_NAME = str(getenv('APP_NAME'))
    else:
        ON_HEROKU = False

    # Web server configuration
    BIND_ADDRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '181.214.152.133'))
    FQDN = str(getenv('FQDN', 'srv31221116.ultasrv.net:65535')) if not ON_HEROKU or getenv('FQDN' 'srv31221116.ultasrv.net:65535') else APP_NAME + '.herokuapp.com'

    # SSL configuration
    HAS_SSL = bool(getenv('HAS_SSL', False))
    if HAS_SSL:
        URL = "https://{}/".format(FQDN)
    else:
        URL = "http://{}/".format(FQDN)

    # Database configuration
    DATABASE_URL = str(getenv('mongodb+srv://Filetolink:yuvraj178@cluster0.focy2ua.mongodb.net/?retryWrites=true&w=majority'))  # Your database connection URL

    # Updates channel (optional)
    UPDATES_CHANNEL = str(getenv('Infinity_XBotz', None))  # Your updates channel username

    # Banned channels (if applicable)
    BANNED_CHANNELS = list(set(int(x) for x in str(getenv("BANNED_CHANNELS", "")).split()))  # List of banned channels
