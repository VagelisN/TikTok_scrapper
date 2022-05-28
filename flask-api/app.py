from flask import Flask, request, jsonify, Response, make_response
import service


app = Flask(__name__)


@app.route("/api/v1/daily", methods=["GET"])
def getDailyChallenges():
    return service.getDailyChallenges()


@app.route("/api/v1/makeCompilation", methods=["GET"])
def getVideo():
    hashtag = request.args.get("hashtag")
    if hashtag:
        video_binary = service.getTopDailyVideo(hashtag=hashtag)
        response = make_response(video_binary)
        response.headers.set('Content-Type', 'video/mp4')
        response.headers.set(
            'Content-Disposition', 'attachment', filename="video.mp4"
        )
        return response
    else:
        return "hashtag url parameter needed"

@app.route("/api/v1/getEvolution", methods=["GET"])
def getChallengeEvolution():
    hashtag = request.args.get("hashtag")
    metric = request.args.get("metric")

    if metric not in ["views", "likes", "shares", "score"]:
        return "wrong metric"

    plot_binary = service.getChallengeEvolution(hashtag, metric)
    response = make_response(plot_binary)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set(
        'Content-Disposition', 'attachment', filename="plot.png"
    )
    return response
    
@app.route("/api/v1/most-improved-challenge", methods=["GET"])
def getMostImprovedChallenges():
    return jsonify(challenges=service.getMostTrendingChallenge())

@app.route("/api/v1/overall-most-popular-challenge-videos", methods=["GET"])
def getOverallMostPopularChallengeVideos():
    return jsonify(videos=service.getOverallMostPopularVideos())

if __name__ == "__main__":
    app.run(debug=True, threaded=False, processes=1)


