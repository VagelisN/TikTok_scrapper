from flask import Flask, request, jsonify, Response, make_response
import service


app = Flask(__name__)


@app.route("/api/v1/daily", methods=["GET"])
def getDailyChallenges():
    return jsonify(service.getDailyChallenges())


@app.route("/api/v1/makeCompilation", methods=["GET"])
def getVideo():
    hashtag = request.args.get("hashtag")
    if hashtag:
        video_binary = service.getTopDailyVideo(hashtag=hashtag)
        return responseWithVideo(video_binary)
    else:
        return "hashtag url parameter needed"

@app.route("/api/v1/getEvolution", methods=["GET"])
def getChallengeEvolution():
    hashtag = request.args.get("hashtag")
    metric = request.args.get("metric")

    if metric not in ["views", "likes", "shares", "score"]:
        return "wrong metric"

    plot_binary = service.getChallengeEvolution(hashtag, metric)
    return responseWithPlot(plot_binary)
    
@app.route("/api/v1/most-improved-challenge", methods=["GET"])
def getMostImprovedChallenges():
    return jsonify(challenges=service.getMostTrendingChallenge())

@app.route("/api/v1/overall-most-popular-challenge-videos", methods=["GET"])
def getOverallMostPopularChallengeVideos():
    return jsonify(videos=service.getOverallMostPopularVideos())

@app.route("/api/v1/daily-crawling-score", methods=["GET"])
def getDailyCrawlingScore():
    plot = service.getDailyCrawlingScore()
    return responseWithPlot(plot)

@app.route("/api/v1/challenge-with-most-videos", methods=["GET"])
def getChallengeWithMostVideos():
    return service.challengeWithMostVideos()


def responseWithPlot(plot):
    response = make_response(plot)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set(
        'Content-Disposition', 'attachment', filename="plot.png"
    )
    return response

def responseWithVideo(video):
    response = make_response(video)
    response.headers.set('Content-Type', 'video/mp4')
    response.headers.set(
        'Content-Disposition', 'attachment', filename="video.mp4"
    )
    return response

if __name__ == "__main__":
    app.run(debug=True, threaded=False, processes=1)


