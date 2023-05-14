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
