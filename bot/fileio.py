# Copyright 2023 pooh
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

