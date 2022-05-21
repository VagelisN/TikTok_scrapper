from TikTokApi import TikTokApi
from pymongo import MongoClient
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


client = MongoClient("mongodb+srv://TikTokApi:3patates@tiktokcluster.vcf8n.mongodb.net/?retryWrites=true&w=majority")
hashtags = []
with TikTokApi(logging_level=logging.DEBUG) as api:
    for x in searchHashtags('challenge', 45): 
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
    print(hashtags)
