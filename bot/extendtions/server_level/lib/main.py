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

# from pprint import pprint
from operator import itemgetter
from pprint import pprint

import yaml

# dict_file = {'userlevel' : [{'userid': 189131516},{'userid2' : 56165161},{'userid3' : 51656165161}]}
from ....fileio import databasessavefile

# coding:utf-8

class manager:
    def __init__(self, initxp, charmuti):
        self.userxp = {}
        self.userlevel = {}
        self.isping = {}
        self.initxp = int(initxp)
        self.charmuti = int(charmuti)

    def registerguild(self, guildid:str):
        if guildid in self.userxp:
            pass
            # print(self.userxp[user])
        else:
            self.userxp[guildid] = {}
        if guildid in self.userlevel:
            pass
        else:
            self.userlevel[guildid] = {}
        if guildid in self.isping:
            pass
        else:
            self.isping[guildid] = {}

    def leaderboard(self, guildid:int):
        sort_dict= dict(sorted(self.userlevel[guildid].items(), key=itemgetter(1), reverse=True))
        return sort_dict

    def hadping(self, guildid:str, user: str):
        if user in self.isping[guildid]:
            return True
        else:
            return False

    def toggleping(self, guildid:str,user:str):
        if user in self.isping[guildid]:
            del self.isping[guildid][user]
            return "OK not pinging you when level up"
        else:
            self.isping[guildid][user] = True
            return "OK pinging you when you level up"


    def xpcal(self, guildid:str ,user: str, message:str):
        p = len(message)
        # print(p)
        point = p * self.charmuti
        if user in self.userxp[guildid]:
            self.userxp[guildid][user] =+ point
            # print(self.userxp[user])
        else:
            self.userxp[guildid][user] = 0

    def checkxp(self, guildid:str, user: str):
        return self.userxp[guildid][user]

    def levelcal(self, guildid:str ,user: str):
        initxp = self.initxp
        if user in self.userlevel[guildid]:
            if self.userlevel[guildid][user] == 0:
                self.userlevel[guildid][user] += 1
                return True
            elif self.userxp[guildid][user] >= initxp and self.userlevel[guildid][user] == 1:
                self.userlevel[guildid][user] += 1
                return True
            else:
                uplv = initxp * self.userlevel[guildid][user]
                b = self.userxp[guildid][user]
                if b >= int(uplv):
                    print('user levevl up')
                    self.userlevel[guildid][user] += 1
                    self.userxp[guildid][user] = 0
                    return True
        else:
            self.userlevel[guildid][user] = 0

    def xpneedlv(self, guildid:str,user:str):
        initxp = 300
        uplv = initxp * self.userlevel[guildid][user]
        return uplv
    def checklevel(self, guildid:str,user: str):
        self.userlevel[guildid][user]
        return self.userlevel[guildid][user]

    def setxp(self, guildid:str,user:str, xp:int ):
        self.userxp[guildid][user] = xp

    def setlevel(self, guildid:str ,user:str, level:int):
        self.userlevel[guildid][user] = level

    def savestate(self):
        save = {}
        save['level'] = self.userlevel
        save['xp'] = self.userxp
        save['ping'] = self.isping
        with open(str(databasessavefile), 'w') as file:
            documents = yaml.dump(save, file)

    def getaload(self):
        a = open(str(databasessavefile))
        levelconf = yaml.load(a, Loader=yaml.FullLoader)
        # pprint(levelconf)
        for idkey, idk in levelconf['level'].items():
            # print(idkey)
            # print(idk)
            self.userlevel[idkey] = idk
        for iakey, ida in levelconf['xp'].items():
            self.userxp[iakey] = ida
        for k, v in levelconf['ping'].items():
            self.isping[k] = v
