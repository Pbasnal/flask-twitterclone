import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask import current_app

from logging_setup.logger import ApiLogger
from loguru import logger

logger.debug(f"current app {current_app.config}")
WATSON_IAMAUTH_KEY = current_app.config["WATSON_IAMAUTH_KEY"]
WATSON_TONE_INSTANCE = current_app.config["WATSON_TONE_INSTANCE"]

authenticator = IAMAuthenticator(WATSON_IAMAUTH_KEY)
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator)

tone_analyzer.set_service_url(f"https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/{WATSON_TONE_INSTANCE}")

def analyze_text(text, flow_id):
    ApiLogger.log_debug(flow_id, "Sentiment analyzer - begin", "")

    tone_analysis = tone_analyzer.tone(
            {'text': text}, 
            content_type='application/json') \
        .get_result()

    ApiLogger.log_debug(flow_id, "Sentiment analyzer - analysis result", json.dumps(tone_analysis))

    sentiments = dict()
    for tone in tone_analysis["document_tone"]["tones"]:
        sentiments[tone["tone_id"]] = tone["score"]
    
    return sentiments