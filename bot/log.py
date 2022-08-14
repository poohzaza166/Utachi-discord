import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',encoding='utf-8',level=logging.INFO)
logs = logging.getLogger(__name__)
