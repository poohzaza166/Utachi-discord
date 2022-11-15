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