from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from models.MongoEngine import MongoDb
from models.UserInteractionSentiment import UserInteractionSentiment, NEW_ENTRY_ADDED, ALREADY_EXISTS
from models.UserOverallSentiments import UserOverallSentiments
from logging_setup.logger import ApiLogger

import sentiment_handlers.add_new_sentiment as sh  # sentiment handlers

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'test_users_db',
    'host': 'localhost',
    'port': 27017
}
MongoDb.init_app(app)


@app.route("/user_sentiment", methods=['GET'])
def get_user_sentiment():
    flow_id = "get user sentiments"
    try:
        userid = request.args.get('userid', type=str)
        contentid = request.args.get('contentid', default=None, type=str)
        towardsuserid = request.args.get(
            'towardsuserid', default=None, type=str)

        ApiLogger.log_debug(flow_id, "Fetching overall sentiments for ",
            f"User_sentiment - parameters userid: {userid} contentid: {contentid}")
        if contentid == None:
            return jsonify(UserOverallSentiments.get_user_sentiment(userid))

        return jsonify(UserInteractionSentiment.get_user_sentiment_for_content(userid, contentid, towardsuserid))
    except:
        logger.exception(flow_id + "Api exception")
        raise


@app.route("/user_sentiment", methods=['POST'])
def set_user_sentiment():
    try:
        flow_id = "set user sentiments"
        ApiLogger.log_debug(flow_id, "Api Begin",
                            f"set user sentiments - {request.json}")
        return jsonify(sh.set_user_sentiment(request.json, flow_id))
    except:
        logger.exception(flow_id + "Api exception")
        raise


@app.route("/check_sentiment", methods=['POST'])
def analyze_sentiment():
    try:
        flow_id = "Analyze sentiment"
        ApiLogger.log_debug(flow_id, "Api Begin", f"{request.json}")

        return jsonify(sh.get_sentiments_of_content(request.json, flow_id))
    except:
        logger.exception(flow_id + "Api exception")
        raise


if __name__ == "__main__":
    logger = ApiLogger.get_logger("logs/sentiment_api.log")
    # sentiments = dict()
    # sentiments["anger"] = 0.89
    # sentiments["sad"] = 0.79
    # sentiments["happy"] = 0.99

    # UserInteractionSentiment.add_if_not_exists("123", "post", "321", "124", sentiments)
    app.run(debug=True)
