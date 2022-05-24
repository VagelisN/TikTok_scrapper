from operator import itemgetter
from TikTokApi import TikTokApi
from pymongo import MongoClient
from datetime import datetime
import logging
import requests
import re

baseUrl = 'https://m.tiktok.com/api/search/general/full/?aid=1988&keyword='  
urlOffSet = '&offset='  
urlEnding ='&verifyFp=verify_l0h7ncp4_Fd2ZmLZO_WHvz_42pj_8zhK_gyZjJYxzHwf9'
headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "cookie-consent={%22ga%22:true%2C%22af%22:true%2C%22fbp%22:true%2C%22lip%22:true%2C%22bing%22:true%2C%22ttads%22:true%2C%22version%22:%22v7%22}; tt_csrf_token=hqZTBFxz-c4p8Fx2lPLGDIcg2gPtrcCOVOvw; passport_csrf_token=b14f92452fa8fb6e38ab44a9903cd165; passport_csrf_token_default=b14f92452fa8fb6e38ab44a9903cd165; _abck=6016451C270901263E7751047EA955D9~-1~YAAQNn7N1EZuH5GAAQAA10U09gf0x5a56s4n2N2VEhaitB2l4ygYyUwPRSp64oP7CDTtme8CVjuYuRxc3P5aZ4fk9UA4gX+OikwoYYN9VrxiVk3iEVsCtktYZ+pPMXTxPWj1CXMCm5rP2aYaMsArUjSnKuaTMF5MkZtSmacp63cZDl3049m8ypu5EKRGsQ61x7R9JVBWOxICjDAvxQPgYDVdQNpB7IyviWpCc0xAtZYElYGriUb0LqYbSuf3oUPSYWcdmWg3XfB2MPIHHusdnBmYBgyhU+hHUgfOLL3j6Wgh6Vv6X1hOEfhGKAcUQMoBO19OXWPbUyZQroWasIjecXKbDWE9aMu/rhZbga/DCWTcEqdX6HG7J9BsXHZ2yzI6eE6OyD965tjQOg==~-1~-1~-1; bm_sz=D06355F29913E47B3F807D61F1B4A790~YAAQNn7N1EluH5GAAQAA10U09g8wpf0h+jngZYhwzZLzrbjl/t6UtsY30+JgqF6sY8BgWUThHPKcK+10JOy2QfCPXh+lRAl7Z/kzG1+g6gPnZvxnetPgGHk1BlfC+zjiQkNeiG5/fJ6JSRjLG/F5QNX8KFFGWtuKkTnE4uS34jp1Q2oLE6KTlVQsRWzXS1oh2SIsY8Tk3qIOLtxrbsHJUx2ffrcvc7rB9IFSSUH5ZrzuKOI47Werd9YbyHxbK/psIT13tRt4zjZ2eL0Ju3iawBVKM4pU11YhpJCyWF+N88S4IW4=~3224129~4342849; bm_mi=DD35F4506F806050EB7B78C5B0D04EAA~YAAQX37N1BKYe5KAAQAA9yc49g8vdohkj0O9XjrRZHTjRaTo5mjY8S1SBGcQVQryJAkfSE5qFH9tY3VPm3tdBWT1fZRP2rjzxhY6MAN9GFTmhibRrG4nQd/MRWixSde+NtGOoINIhxOG61DDiFmm04RvKWernE+rOGfgzirLlsGlx8qh20XFcLcd8KxJfXZP7xwsiHfYeVgrXyr7q03Vo5RN9hrQuTQDfF3C1sxrG0MAnIJe2zm/lTq4OeiC8rgqhEBrA1stFQ7sJZOgEDW1ffUHnh7Ij/uGd7Ui1iyDr5uc9gVxVj0RGh0CYuur/HaugW47~1; bm_sv=011CD9A14C2A164E7880964AA0850D74~YAAQX37N1BOYe5KAAQAA9yc49g/vzUok4I+urXz9LcG48flgKJA5wT6R8UulBCsLteKajsdSNuRhU6RZhGW0drhMkd2V8sRqIvNJrKW3KQ67qUu/aTytVcMMl7iHatQQ0iLE1AJ0gwZiOM0Js9gCFpvS4HXmBQb759Ez6qdKHH6zQWOQI62lloBXhgML3aO/mSgNzPmi0pnoFRE6viHh+yqxG4/prOopSHDrfavRCpmGERRwfvaFpAEaBjBzA6po~1; ak_bmsc=055333B58567BAEFB2C04BB29A69C60C~000000000000000000000000000000~YAAQPH7N1Al7DuOAAQAApHI59g9yPLaLoJCLMBKCo5+25iUQYXZ9AYWL1KpN9c7m0dSSHlCLmqV8thlhuG/A6Rbq47HnMbDroEzkwRf07460rMmDUb6RFOlmkFX3RIuZ3lfDctNFhu/m9rYHuoXi82Vuk9Kie1eAkaovb0bsmlRI7GDtPcTI6iEysl8RoKB4kXbkGhB01gl/yqYgfpxmtPlVr4RqyhCWoVB3QsPZKMQE6gmrfnJ1JR4dqq4ixtZJHrSgbCyc8NlhtYXXEwhBGWqAodI/AO48xEn5o9vCtXSeigvQEIlIofIEmPyC5KLPIBo4vefC33KpoMFlMmhxFSy2JM3ap14oRIN4jJ4Drg+XqRJiKRs+7CVnLbu5gI/zKSWK42KbZHYzR+yDm7B8uFS1ucBTtgdDJolYzo8XRF317kA=; cmpl_token=AgQQAPOfF-RO0rJwefQrdt08-EfuektJP4cUYMfjxA; sid_guard=4759ee2ecac14c7f1a82025e25145c10%7C1653399372%7C5184000%7CSat%2C+23-Jul-2022+13%3A36%3A12+GMT; uid_tt=e6dae8f991d5a9f174ef2d475d41422b5b82395e8c2929653b4a1eee79bdae59; uid_tt_ss=e6dae8f991d5a9f174ef2d475d41422b5b82395e8c2929653b4a1eee79bdae59; sid_tt=4759ee2ecac14c7f1a82025e25145c10; sessionid=4759ee2ecac14c7f1a82025e25145c10; sessionid_ss=4759ee2ecac14c7f1a82025e25145c10; sid_ucp_v1=1.0.0-KGNjNjY5ZWExMzQ5M2Q4Y2JkNjViOWM0ODY3ZGZiNWNkOTVhM2U1MDYKIAiFiJCauuqlp2IQzL6zlAYYswsgDDDmrrqSBjgBQOoHEAMaBm1hbGl2YSIgNDc1OWVlMmVjYWMxNGM3ZjFhODIwMjVlMjUxNDVjMTA; ssid_ucp_v1=1.0.0-KGNjNjY5ZWExMzQ5M2Q4Y2JkNjViOWM0ODY3ZGZiNWNkOTVhM2U1MDYKIAiFiJCauuqlp2IQzL6zlAYYswsgDDDmrrqSBjgBQOoHEAMaBm1hbGl2YSIgNDc1OWVlMmVjYWMxNGM3ZjFhODIwMjVlMjUxNDVjMTA; store-idc=maliva; store-country-code=gr; tt-target-idc=useast1a; ttwid=1%7Cjcz9UOHEAxXYCfYyRfi2LuvaMtT9XZHXCqkUxL51Byo%7C1653399376%7C59497409900d6d53fbc67311b1493cf0aaa62e8f7e82326d028865878f680c06; odin_tt=067be1aeb67b8a07a60c1877f39defbb916a7df7c659dd90e85f2057e7d7dfe1e2c1216a523349bfcf77cdcc7087d2eab723cb65046c6322adb24bf9abf5f8a26d7a504c19057691d2e2512626b107b5; msToken=iN4QpRqzGooyhrEKMgMKN2Smqzjh_I5IVz7D-nFX4tvktR4qLNPJLjdXp2bB28vu95Ss6mdqINGc-Pi459LZqMBpsPMJ2jOZzavt_zKnsn95zgaKr6oLUP9tq5ms9SraVwPLnKPh"
    }

def getPopularChallengeHashtags(name):
    challenges = set()
    offset = 0
    while offset <= 100:
        # %23 is the url encoding of '#'
        response = requests.get(baseUrl + '%23' + name + urlOffSet + str(offset) + urlEnding, headers= headers).json()
        for data in response['data']:
            if 'item' not in data.keys() or 'textExtra' not in data['item']:
                continue
            for challenge in data["item"]["textExtra"]:
                tmp = challenge["hashtagName"]
                tmp = tmp.lower()
                if tmp != 'challenge' and tmp != 'challenges' and 'challenge' in tmp and not isHashtagContainedInDb(tmp):
                    challenges.add(tmp)
        offset += 12
    return challenges

def isHashtagContainedInDb( hashtag):
    result = list(dailyTrendsCollection.find({
        'name': hashtag,
        'date': datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    }))
    if len(result) == 0:
        return False
    else:
        return True

def getTopVideosForHashtag(name):
    videos = []
    offset = 0
    while offset <= 100:
        response = requests.get(baseUrl + name + urlOffSet + str(offset) + urlEnding, headers= headers).json()
        if 'data' not in response.keys():
            break
        for data in response['data']:
            if 'item' not in data.keys() or 'textExtra' not in data['item']:
                continue
            item = data["item"]
            if True in [True if name == x['hashtagName'] else False  for x in item['textExtra']]:
                pass
            else:
                continue

            id = item['video']['id']
            likes = item['stats']['diggCount']
            shares = item['stats']['shareCount']
            views = item['stats']['playCount']
            video_score = views + 1.6 * likes + 2.2 * shares
            videos.append({"id" : id, "score" : video_score, "likes": likes, "views": views, "shares": shares})  
        offset += 12
    return sorted(videos, key=itemgetter('score'), reverse=True)[:5]

def getVideoFromId( videoId):
    return api.video(id = videoId)

def getUsersVideos(username):
    response = requests.get('https://tiktok.com/@' + username, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36'}).text
    compileStr = '"user-post"(?:.)*?"browserList"'
    p = re.compile(compileStr, re.DOTALL)
    trimmedResponse = p.search(response).group(0)
    p = re.compile('\d+')
    results = []
    for id in p.findall(trimmedResponse):
        results.append(id)
    return results

def getChallengeHashtagsFromVideo(video):
    results = []
    challenges = video.hashtags
    for challenge in challenges:
        name = challenge.name
        if (name != 'challenge') and (name != 'challenges') and ('challenge' in name):
            results.append(name)
    return results

'''
Returns the challenge, with the 5 most popular videos
'''
def getSumForHashtag(hashtagName):
    if isinstance(hashtagName, list):
        hashtagName = hashtagName[0]
    topVideos = getTopVideosForHashtag(hashtagName)

    totalLikes = sum(i['likes'] for i in topVideos)
    totalShares = sum(i['shares'] for i in topVideos)
    totalViews = sum(i['views'] for i in topVideos)
    totalScore = sum(i['score'] for i in topVideos)
    return {
        "name": hashtagName, 
        "date": datetime.today().replace(hour=0, minute=0, second=0, microsecond=0),
        "likes" : totalLikes, 
        "views": totalViews, 
        "shares": totalShares, 
        "score": totalScore, 
        "videos": topVideos
    }


client = MongoClient("mongodb+srv://TikTokApi:3patates@tiktokcluster.vcf8n.mongodb.net/?retryWrites=true&w=majority")
tikTokDB = client['TikTokDB']
dailyTrendsCollection = tikTokDB['DailyTrends']
hashtags = []
customVerify = "verify_l0h7ncp4_Fd2ZmLZO_WHvz_42pj_8zhK_gyZjJYxzHwf9"
deviceId = 'ac0c4016-b6c1-4f57-ab70-5714df68782c'
with TikTokApi(logging_level=logging.DEBUG, custom_verify_fp= customVerify, generate_static_device_id=True) as api:
    hashtags = getPopularChallengeHashtags('challenge')
    '''
    For each separate hashtag in list, get 100 videos, 
    and keep the top 5 based on the following formula
    VC + LC * 1.6 + SC * 2.2
    '''
    print(hashtags)
    for hashtag in hashtags:
        item = getSumForHashtag(hashtag) 
        print(item)
        dailyTrendsCollection.insert_one(item)