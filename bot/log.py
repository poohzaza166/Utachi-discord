import logging
from . import fileio

botconfig = fileio.botconfig


if botconfig['bot_setting']['loglevel'] == "debug":
    logging.basicConfig(filename='config/app.log', filemode='w',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s ',encoding='utf-8',level=logging.DEBUG)

elif botconfig['bot_setting']['loglevel'] == "info":
    logging.basicConfig(filename='config/app.log', filemode='w',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s ',encoding='utf-8',level=logging.INFO)

elif botconfig['bot_setting']['loglevel'] == "error":
    logging.basicConfig(filename='config/app.log', filemode='w',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s ',encoding='utf-8',level=logging.ERROR)


logs = logging.getLogger(__name__)
