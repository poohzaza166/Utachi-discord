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

from ....fileio import botconfig
from ....log import logs

# apiA = str(botconfig['bot_setting']['youtubeapiA'])
# apiB = str(botconfig['bot_setting']['youtubeapiB'])
# apiC = str(botconfig['bot_setting']['youtubeapiC'])

# class ytkey:
#     def __init__(self,keyA,keyB,keyC):
#         self.keyA = keyA
#         self.keyB = keyB
#         self.keyC = keyC
#         self.currentkey = ''

#     def defaults(self):
#         self.currentkey = self.keyA

#     def changekey(self):
#         if self.currentkey == self.keyA:
#             self.currentkey = self.keyB
#             logs.debug(self.currentkey)
#         elif self.currentkey == self.keyB:
#             self.currentkey = self.keyC
#             logs.debug(self.currentkey)
#         elif self.currentkey == self.keyC:
#             self.currentkey = self.keyA
#             logs.debug(self.currentkey)

#     def getkey(self):
#         return str(self.currentkey)

class ytkey:
    def __init__(self,keylist):
        self.keylist = tuple(keylist)
        self.currentkey = ''

    def defaults(self):
        self.currentkey = self.keylist[0]
        logs.info(self.currentkey)

    def changekey(self):
        a = self.keylist.index(self.currentkey)
        if a == len(self.keylist):
            self.currentkey = self.keylist[0]
            logs.info(self.currentkey)
        else:
            self.currentkey = self.keylist[a+1]
            logs.info(self.currentkey)

    def getkey(self):
        return str(self.currentkey)

ApiKeys = ytkey(botconfig['bot_setting']['ytkey'])

# ApiKeys = ytkey(keyA=apiA,keyB=apiB,keyC=apiC)
ApiKeys.defaults()
# if __name__ != '__main__':
