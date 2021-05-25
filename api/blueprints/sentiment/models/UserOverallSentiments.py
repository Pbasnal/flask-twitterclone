import json
from api.models.MongoEngine import dbcontext
from logging_setup.logger import ApiLogger

class UserOverallSentiments(dbcontext.Document):
    # User whose content, comment or msg is being analyzed
    user_id = dbcontext.StringField(required=True)

    # Sentiments of user in general on the platform
    sentiments = dbcontext.DictField()
    sentiments_count = dbcontext.IntField()

    # Sentiments of user in general in the content that user has created
    sentiments_in_contents = dbcontext.DictField()
    sentiments_in_contents_count = dbcontext.IntField()

    # Sentiments of user in general in the comments
    sentiments_in_comments = dbcontext.DictField()
    sentiments_in_comments_count = dbcontext.IntField()

    # Sentiments of user in general in the private messages
    sentiments_in_messages = dbcontext.DictField()
    sentiments_in_messages_count = dbcontext.IntField()

    def ToJsonString(self):
        return "{ \
            \"user_id\": \"" + self.user_id + "\", \
            \"sentiments\": " + json.dumps(self.sentiments) + ", \
            \"sentiments_count\": \"" + str(self.sentiments_count) + "\", \
            \"sentiments_in_contents\": " + json.dumps(self.sentiments_in_contents) + ", \
            \"sentiments_in_contents_count\": \"" + str(self.sentiments_in_contents_count) + "\", \
            \"sentiments_in_comments\": " + json.dumps(self.sentiments_in_comments) + ", \
            \"sentiments_in_comments_count\": \"" + str(self.sentiments_in_comments_count) + "\", \
            \"sentiments_in_messages\": " + json.dumps(self.sentiments_in_messages) + ", \
            \"sentiments_in_messages_count\": \"" + str(self.sentiments_in_messages_count) + "\", \
        }"

    @staticmethod
    def get_user_sentiment(userid):
        logger = ApiLogger.get_logger()
        logger.debug(f"Getting users overall sentiment")
        try:
            return UserOverallSentiments.objects(user_id=userid).get()
        except dbcontext.DoesNotExist:
            logger.debug(f"User does not exists {userid}")
        return None

    @staticmethod
    def add_or_update(user_id, sentiments, content_type, flow_id):
        ApiLogger.log_debug(flow_id, "Overall sentiment - add_or_update", "")

        user_sentiments = None
        try:
            user_sentiments = UserOverallSentiments.objects(
                user_id=user_id).get()
        except dbcontext.DoesNotExist:
            ApiLogger.log_debug(
                flow_id, "Overall sentiment - user doesn't exists", f"user data doesn't exist, inserting")

        if user_sentiments is not None:
            UserOverallSentiments.update_user_sentiments(
                user_sentiments,
                sentiments,
                content_type,
                flow_id)
        else:
            user_sentiments = UserOverallSentiments.add_user_sentiments(
                user_id,
                user_sentiments,
                sentiments,
                content_type,
                flow_id)

        user_sentiments.save()
        return user_sentiments

    @staticmethod
    def add_user_sentiments(user_id, user_sentiments, sentiments, content_type, flow_id):
        ApiLogger.log_debug(flow_id, "Add user sentiment - Begin", "")

        input_args = {
            "user_id": user_id,
            "user_sentiments": user_sentiments,
            "sentiments": sentiments,
            "content_type": content_type
        }
        ApiLogger.log_debug(
            flow_id, "Add user sentiment - args", json.dumps(input_args))

        sentiments_in_contents = dict()
        sentiments_in_comments = dict()
        sentiments_in_messages = dict()

        sentiments_in_contents_count = 0
        sentiments_in_comments_count = 0
        sentiments_in_messages_count = 0

        if content_type == "content":
            sentiments_in_contents = sentiments
            sentiments_in_contents_count = 1
        elif content_type == "comment":
            sentiments_in_comment = sentiments
            sentiments_in_comments_count = 1
        elif content_type == "message":
            sentiments_in_message = sentiments
            sentiments_in_messages_count = 1

        return UserOverallSentiments(
            user_id=user_id,
            sentiments=sentiments,
            sentiments_in_contents=sentiments_in_contents,
            sentiments_in_comments=sentiments_in_comments,
            sentiments_in_messages=sentiments_in_messages,

            sentiments_count=1,
            sentiments_in_contents_count=sentiments_in_contents_count,
            sentiments_in_comments_count=sentiments_in_comments_count,
            sentiments_in_messages_count=sentiments_in_messages_count)

    @staticmethod
    def update_user_sentiments(user_sentiments, sentiments, content_type, flow_id):
        ApiLogger.log_debug(flow_id, "Update user sentiment - begin", "")

        input_args = {
            "user_sentiments": user_sentiments,
            "sentiments": sentiments,
            "content_type": content_type
        }
        
        ApiLogger.log_debug(
            flow_id, "Update user sentiment - args", "{ \
                    \"user_sentiments\": " + user_sentiments.ToJsonString() + ", \
                    \"sentiments\": " + json.dumps(sentiments) + ", \
                    \"content_type\": \"" + content_type + "\" \
                }")

        user_sentiments.sentiments_count = UserOverallSentiments.update_sentiments_dict(
            user_sentiments.sentiments,
            sentiments,
            user_sentiments.sentiments_count, flow_id)

        if content_type == "content":
            ApiLogger.log_debug(
                flow_id, "Update user sentiment - begin", "adding sentiment for content")

            user_sentiments.sentiments_in_contents_count = UserOverallSentiments.update_sentiments_dict(
                user_sentiments.sentiments_in_contents,
                sentiments,
                user_sentiments.sentiments_in_contents_count, flow_id)

        elif content_type == "comment":
            ApiLogger.log_debug(
                flow_id, "Update user sentiment - begin", "adding sentiment for comment")

            user_sentiments.sentiments_in_comments_count = UserOverallSentiments.update_sentiments_dict(
                user_sentiments.sentiments_in_comments,
                sentiments,
                user_sentiments.sentiments_in_comments_count, flow_id)

        elif content_type == "message":
            ApiLogger.log_debug(
                flow_id, "Update user sentiment - begin", "adding sentiment for message")

            user_sentiments.sentiments_in_messages_count = UserOverallSentiments.update_sentiments_dict(
                user_sentiments.sentiments_in_messages,
                sentiments,
                user_sentiments.sentiments_in_messages_count, flow_id)

    @staticmethod
    def update_sentiments_dict(values, new_values, count, flow_id):

        ApiLogger.log_debug(
            flow_id, "Update user sentiments dict", f"new_values: {json.dumps(new_values)}  -  values: {json.dumps(values)}")
        for sentiment in new_values:
            if sentiment not in values:
                values[sentiment] = 0
            values[sentiment] = (count * values[sentiment] +
                                 new_values[sentiment]) / (count + 1)

        return count + 1
