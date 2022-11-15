import os

import yaml

# from .log import logs

is_conainer = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
docker_token = os.environ.get('token',None)
docker_admin_acc = os.environ.get('adminacc',None)
docker_bot_prefix = os.environ.get('bot_prefix', None)

databasessavefile = 'config/database.yaml'
# databasessavefile = 'database.yaml'

try:
    seting = open('config/botsetting.yaml')
    # a = open('botsetting.yaml')
    botconfig = yaml.load(seting, Loader=yaml.FullLoader)
except FileNotFoundError as error:
    # logs.debug(error)
    # logs.info('no config file found genreating new one')
    print('no config file found')
except yaml.YAMLError as exc:
    print('config file error ')
    if hasattr(exc, 'problem_mark'):
        mark = exc.problem_mark
        print(f"Error position: (%s:%s)" % (mark.line+1, mark.column+1))

# Error position: (1:22)

