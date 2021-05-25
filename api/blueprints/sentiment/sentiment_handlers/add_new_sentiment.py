from ..models.UserInteractionSentiment import UserInteractionSentiment, NEW_ENTRY_ADDED, ALREADY_EXISTS
from ..models.UserOverallSentiments import UserOverallSentiments
from logging_setup.logger import ApiLogger

from ..sentiment_analyzer.tone import analyze_text

def set_user_sentiment(input_data, flow_id):
    ApiLogger.log_debug(flow_id, "Sentiment Handler - Set", f"set_user_sentiments - {input_data}")

    input_data["sentiments"] = get_sentiments_of_content(input_data, flow_id)
    user_sentiment, new_or_not = insert_user_interaction(input_data, flow_id) 

    if new_or_not is NEW_ENTRY_ADDED:
        update_overall_sentiments(input_data, flow_id)

    return [input_data, new_or_not]

def update_overall_sentiments(input_data, flow_id):
    ApiLogger.log_debug(flow_id, "Update overall sentiment", "set_user_sentiments - Updating overall sentiment of the user")
    
    user_sentiments = UserOverallSentiments \
        .add_or_update(input_data["userid"],
            input_data["sentiments"],
            input_data["content-type"],
            flow_id)

def insert_user_interaction(input_data, flow_id):
    ApiLogger.log_debug(flow_id, "Insert user sentiment", "set_user_sentiments - Inserting sentiment data in user_interactions")

    return UserInteractionSentiment.add_if_not_exists(input_data["userid"], 
        input_data["content-type"], 
        input_data["contentid"], 
        input_data["towards-userid"], 
        input_data["sentiments"])

def get_sentiments_of_content(input_data, flow_id):
    ApiLogger.log_debug(flow_id, "Insert user sentiment", "set_user_sentiments - fetching sentiments from watson")

    ## TODO: add the api calls
    return analyze_text(input_data["content"], flow_id)