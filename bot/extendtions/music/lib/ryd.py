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

import requests

def makereq(url: str):
    vidid = url.replace('https://www.youtube.com/watch?v=', '')
    # vidid = 'LZWKYShMsus'
    data = requests.get(f'https://returnyoutubedislikeapi.com/votes?videoId={vidid}')
    try:
        a = data.json()['dislikes']
        # print(a)
        return f'data provided by project return youtube dislike project \n This video have a dislike count of {a}'
    except KeyError:
        return 'no video dislike data founded in return youtube dislike project database'


if __name__ == '__main__':
    print(makereq('https://www.youtube.com/watch?v=sXQxhojSdZM'))