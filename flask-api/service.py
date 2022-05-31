from cmath import inf
from operator import itemgetter
from re import L
import pymongo
import utils
import math
from datetime import datetime
from bson.json_util import dumps


def getDailyChallenges():
    '''
    Return today's 5 top scoring challenges
    '''
    # connect to db
    db = __connectToDB("TikTokDB")
    collection = db.DailyTrends

    # find items with date equal to today
    cursor = collection.find({
        "date" : {
            "$eq": datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        }},
        { "name" : 1, "_id" : 0, "score": 1 }  # selected fields
    ).sort("score", -1).limit(5)
    return [doc for doc in cursor]


def getTopDailyVideo(hashtag):
    # connect to db
    db = __connectToDB("TikTokDB")
    collection = db.DailyTrends

    # find items with date equal to today
    cursor = collection.find({
        "date" : {
            "$eq": datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        },
        "name" : hashtag
        },
        {"_id" : 0, "videos": { "id": 1} }  # selected fields
    ).sort("score", -1).limit(1)
    
    videos = cursor.next()
    id_list = [video["id"] for video in videos["videos"]]
    return utils.makeCompilation(id_list)


def getChallengeEvolution(hashtag, metric):
    # connect to db
    db = __connectToDB("TikTokDB")
    collection = db.DailyTrends
    # find entries of hashtag with ascending date
    cursor = collection.find({
        "name" : hashtag
        },
        {"_id" : 0, "videos": 0}  # selected fields
    ).sort("date", 1)

    data = utils.makePlotAndGetBinary(cursor, hashtag, metric)
    return data


'''
Gets all challenges with at least two days of data.
Returns the one with the biggest increase in score between
the last metric and the first one.
'''
def getMostTrendingChallenge() -> dict:
    db = __connectToDB("TikTokDB")
    collection = db.DailyTrends
    # find items with date equal to today
    cursor = collection.find({},{}).sort([("name", 1), ('date', 1)])
    
    challenges = dict()
    for i in cursor: 
        name = i['name']
        if name not in challenges.keys():
            challenges[name] = [i]
        else:
            challenges[name].append(i)
    return __calculateGainedScore(challenges)[:5]


def getOverallMostPopularVideos():
    db = __connectToDB("TikTokDB")
    collection = db.DailyTrends
    encounteredVideos = {}
    cursor = collection.find({},{"_id": 0 ,"date": 1, "videos": 1})
    for i in cursor:
        videos = i['videos']
        for vid in videos:
            if vid['id'] not in encounteredVideos.keys():
                encounteredVideos[vid['id']] = vid['score']
            elif vid['score'] > encounteredVideos[vid['id']]:
                encounteredVideos[vid['id']] = vid['score']
    mostPopular = sorted(encounteredVideos.items(), key= lambda item: item[1], reverse= True)[:10]
    return [i[0] for i in mostPopular]

def getDailyCrawlingScore():
    db = __connectToDB("TikTokDB")
    collection = db.DailyTrends
    dailyScores = dict()
    cursor = collection.find({},{"_id": 0 ,"name": 1, 'date': 1 , "score": 1}).sort('date', 1)
    for i in cursor:
        date = i['date']
        score = int(i['score'])
        if date not in dailyScores.keys():
            dailyScores[date] = score
        else:
            prevScore = dailyScores[date]
            dailyScores[date] = prevScore + score
    return utils.plotCrawlingProgress(dailyScores)

def getAllChallenges():
    db = __connectToDB("TikTokDB")
    collection = db.DailyTrends
    cursor = collection.find({}, {"_id": 0, "name": 1, "date": 1, "score": 1}).sort('date', 1)
    return [i for i in cursor]

def getDistinctChallenges():
    db = __connectToDB("TikTokDB")
    collection = db.DailyTrends
    cursor = collection.find({}, {"_id": 0, "name": 1})
    results = set()
    for i in cursor:
        results.add(i['name'])
    return {"names": [i for i in  results], 'count': len(results) }

def __calculateGainedScore(challenges: dict) -> list:
    scores = list()
    for key in challenges.keys():
        minScore, minViews, minLikes, minShares = math.inf, math.inf, math.inf, math.inf
        maxScore, maxViews, maxLikes, maxShares = 0, 0, 0, 0
        name: str
        for item in challenges[key]:
            score = item['score']
            views = item['views']
            likes = item['likes']
            shares = item['shares']
            name = item['name']
            if score < minScore:
                minViews, minLikes, minShares, minScore = views, likes, shares, score
            if score > maxScore:
                maxViews, maxLikes, maxShares, maxScore = views, likes, shares, score
        difference = maxScore - minScore
        if difference > 0:
            scores.append({'name': name, 'minScore': int(minScore), 'maxScore': int(maxScore), 'difference': int(difference), 'likesGained': int(maxLikes - minLikes), 'viewsGained': int(maxViews - minViews), 'sharesGained': int(maxShares - minShares)})
    return sorted(scores, key=itemgetter('difference'), reverse=True)

def __connectToDB(name):
    try:
        client = pymongo.MongoClient("mongodb+srv://TikTokApi:3patates@tiktokcluster.vcf8n.mongodb.net/?retryWrites=true&w=majority")
        db = client[f"{name}"]
        return db
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        
def challengeWithMostVideos():

    db = __connectToDB("TikTokDB")
    collection = db.DailyTrends

    pipeline = [
    {"$unwind": "$videos"},
    {"$group": {
        "_id" : "$name",
        "uniqueCount": {"$addToSet": "$videos.id"}
        }},
    {"$project": {"_id": 0, "name": "$_id", "uniqueVideoCount": {"$size": "$uniqueCount"}}},
    {"$sort": {"uniqueVideoCount" : -1}},
    {"$limit": 1}
    ]

    cursor = collection.aggregate(pipeline)
    return cursor.next()
 