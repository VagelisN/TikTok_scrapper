import pymongo
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