import logging
from . import fileio

botconfig = fileio.botconfig

if botconfig['bot_setting']['loglevel'] == "debug":
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',encoding='utf-8',level=logging.DEBUG)

elif botconfig['bot_setting']['log_level'] == "info":
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',encoding='utf-8',level=logging.INFO)

elif botconfig['bot_setting']['log_level'] == "error":
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',encoding='utf-8',level=logging.ERROR)

logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%H:%M:%S %d-%m-%Y")

logs = logging.getLogger(__name__)
