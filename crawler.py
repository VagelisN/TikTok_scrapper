from operator import itemgetter
from TikTokApi import TikTokApi
from pymongo import MongoClient
from datetime import date
import logging
import requests
import re

def searchHashtags(name, numOfResults):
    return list(api.hashtag(name = name).videos(count= numOfResults))

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
def getTopVideosForHashtag(hashtagName):
    if isinstance(hashtagName, list):
        hashtagName = hashtagName[0]
    allVideos = []
    for x in searchHashtags(hashtagName, 20):
        views = x.as_dict['stats']['playCount']
        likes = x.as_dict['stats']['diggCount']
        shares = x.as_dict['stats']['shareCount']
        video_score = views + 1.6 * likes + 2.2 * shares
        allVideos.append({"id" : x.id, "score" : video_score, "likes": likes, "views": views, "shares": shares})
    topVideos = sorted(allVideos, key=itemgetter('score'), reverse=True)[:4]

    totalLikes = sum(i['likes'] for i in topVideos)
    totalShares = sum(i['shares'] for i in topVideos)
    totalViews = sum(i['views'] for i in topVideos)
    totalScore = sum(i['score'] for i in topVideos)
    return {"name": hashtagName, "date": date.today().strftime("%m/%d/%Y"), "likes" : totalLikes, "views": totalViews, "shares": totalShares, "score": totalScore, "videos": topVideos}


client = MongoClient("mongodb+srv://TikTokApi:3patates@tiktokcluster.vcf8n.mongodb.net/?retryWrites=true&w=majority")
tikTokDB = client['TikTokDB']
dailyTrendsCollection = tikTokDB['DailyTrends']
hashtags = []
customVerify = "verify_l0h7ncp4_Fd2ZmLZO_WHvz_42pj_8zhK_gyZjJYxzHwf9"
deviceId = 'ac0c4016-b6c1-4f57-ab70-5714df68782c'
with TikTokApi(logging_level=logging.DEBUG, custom_verify_fp= customVerify, custom_device_id= deviceId) as api:
    for x in searchHashtags('challenge', 35): 
        '''
        We need to get each specific hashtag that contains 
        the word 'challenge', without being an exact match
        '''
        temp = getChallengeHashtagsFromVideo(x)
        if temp : hashtags.append(temp) 

        '''
        For each separate hashtag in list, get 100 videos, 
        and keep the top 5 based on the following formula
        VC + LC * 1.6 + SC * 2.2
        '''
        
        ''' 
        Then insert each challenge to DB
        '''
    for hashtag in hashtags:
        item = getTopVideosForHashtag(hashtag) 
        print(item)
        dailyTrendsCollection.insert_one(item)
