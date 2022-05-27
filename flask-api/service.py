import pymongo
import utils
from datetime import datetime
from bson.json_util import dumps

def connectToDB(name):
    try:
        client = pymongo.MongoClient("mongodb+srv://TikTokApi:3patates@tiktokcluster.vcf8n.mongodb.net/?retryWrites=true&w=majority")
        db = client[f"{name}"]
        return db

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)




def getDailyChallenges():
    '''
    Return today's 5 top scoring challenges
    '''

    # connect to db
    db = connectToDB("TikTokDB")
    collection = db.DailyTrends

    # find items with date equal to today
    cursor = collection.find({
        "date" : {
            "$eq": datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        }},
        { "name" : 1, "_id" : 0, "score": 1 }  # selected fields
    ).sort("score", -1).limit(5)

    # convert to json
    json_data = dumps(cursor)

    return json_data



def getTopDailyVideo(hashtag):
    # connect to db
    db = connectToDB("TikTokDB")
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
    db = connectToDB("TikTokDB")
    collection = db.DailyTrends

     # find entries of hashtag with ascending date
    cursor = collection.find({
        "name" : hashtag
        },
        {"_id" : 0, "videos": 0}  # selected fields
    ).sort("date", 1).limit(1)

    data = utils.makePlotAndGetBinary(cursor, hashtag, metric)

    return data


