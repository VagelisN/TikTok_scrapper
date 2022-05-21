from flask import Flask, request
from service import *


app = Flask(__name__)

connectToDB("TikTokDB")


@app.route("/api/v1/daily", methods=["GET"])
def getDailyChallenges():
    return displayMalakies()


@app.route("/api/v1/makeCompilation", methods=["GET"])
def makeCompilation():
    hashtag = request.args.get("hashtag")
    return f'hashtag given {hashtag}'





if __name__ == "__main__":
    app.run(debug=True)


