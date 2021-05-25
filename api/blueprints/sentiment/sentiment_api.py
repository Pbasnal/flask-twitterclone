from flask import Blueprint, request, jsonify

from logging_setup.logger import ApiLogger
from ..application.application_api import app_token_required
from .sentiment_handlers import add_new_sentiment as sh
from .models.UserOverallSentiments import UserOverallSentiments
from .models.UserInteractionSentiment import UserInteractionSentiment

sentiment_bp = Blueprint(
    "sentiment_api", 
    __name__,
    url_prefix='/sentiment',
    template_folder='templates/sentiment')

@app_token_required
@sentiment_bp.route("/<userid>", methods=['POST'])
def get_user_sentiment(userid, contentid):
    flow_id = "get_user_sentiments".upper()
    try:
        contentid = request.args.get('contentid', default=None, type=str)
        towardsuserid = request.args.get(
            'towardsuserid', default=None, type=str)

        ApiLogger.log_debug(flow_id, "Fetching overall sentiments for ",
            f"User_sentiment - parameters userid: {userid} contentid: {contentid}")
        if contentid == None:
            return jsonify(UserOverallSentiments.get_user_sentiment(userid))

        return jsonify(UserInteractionSentiment.get_user_sentiment_for_content(userid, contentid, towardsuserid))
    except:
        ApiLogger.log_exception(flow_id, "Api exception", "")
        raise

@app_token_required
@sentiment_bp.route("/", methods=['POST'])
def set_user_sentiment():
    try:
        flow_id = "set_user_sentiments".upper()
        req = request
        ApiLogger.log_debug(flow_id, "Api Begin",
                            f"set user sentiments - {request.json}")
        return jsonify(sh.set_user_sentiment(request.json, flow_id))
    except:
        ApiLogger.log_exception(flow_id, "Api exception", "")
        raise

@app_token_required
@sentiment_bp.route("/check", methods=['POST'])
def analyze_sentiment():
    try:
        flow_id = "Analyze_sentiment".upper()
        ApiLogger.log_debug(flow_id, "Api Begin", f"{request.json}")

        return jsonify(sh.get_sentiments_of_content(request.json, flow_id))
    except:
        ApiLogger.log_exception(flow_id, "Api exception", "")
        raise
