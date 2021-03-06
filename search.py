from itertools import count
from TikTokApi import TikTokApi
#from TiktokApi import *
import logging
import requests
import re

verifyFP = 'verify_l0h7ncp4_Fd2ZmLZO_WHvz_42pj_8zhK_gyZjJYxzHwf9'

'''
If author is defined, then the method returns only the videos uploaded by the specified author
otherwise returns every video.
'''
def searchVideos(title, numOfResults, author = None):
    videos = api.search.videos(search_term=title, count=numOfResults)
    results = []
    for video in videos:
        if author == None or video.author.as_dict['uniqueId'] == author:
            results.append(video)
    return results

'''
If username is defined, then the method returns only that user
otherwise returns a list of users with similar usernames.
'''
def searchUsers(name, numOfResults, username = None):
    users = api.search.users(name, count=numOfResults)
    results = []
    for user in users:
        if username == None or user.as_dict['user_info']['unique_id'] == username:
            results.append(user)
    return results

def searchHashtags(name, numOfResults):
    return list(api.hashtag(name = name).videos(count= numOfResults))

def getUsersVideos( username):
    response = requests.get('https://tiktok.com/@' + username, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36'}).text
    compileStr = '"user-post"(?:.)*?"browserList"'
    p = re.compile(compileStr, re.DOTALL)
    trimmedResponse = p.search(response).group(0)
    p = re.compile('\d+')
    results = []
    for id in p.findall(trimmedResponse):
        results.append(id)
    return results


with TikTokApi(logging_level=logging.DEBUG, custom_verify_fp=verifyFP) as api:
    for user in searchUsers('therock', 1, 'therock'):
        print(user.as_dict['user_info']['unique_id'])
    print('----------------------------------------------------')
    for x in searchVideos(title = 'therock', numOfResults = 1, author = 'therock'):
        #print(x.as_dict.keys())
        print(x.as_dict['id'])
        print(x.as_dict['stats']['playCount'])
        print(x.as_dict['duetEnabled'])
        print(x.as_dict['stitchEnabled'])
        print(x.hashtags)
    print('----------------------------------------------------')
    for x in searchHashtags('kareas', 5): print(x)
    





    

