import json

from api.models.MongoEngine import dbcontext
from logging_setup.logger import ApiLogger


NEW_ENTRY_ADDED = True
ALREADY_EXISTS = False

class UserInteractionSentiment(dbcontext.Document):
    
    # User whose content, comment or msg is being analyzed
    user_id = dbcontext.StringField(required=True)

    # In case of comment - This is the user who created the content
    # In case of message - This is the user to whom the message is sent
    # In case of post    - This is a tricy scenario. If we can identify that
    #                      a user was targetted, then that user otherwise None
    towards_user = dbcontext.StringField(required=True)

    # This is content, comment or message
    content_type = dbcontext.StringField(required=True)

    content_id = dbcontext.StringField(required=True)

    sentiments = dbcontext.DictField()

    @staticmethod
    def get_user_sentiment_for_content(userid, contentid, towardsuserid=None):
        logger = ApiLogger.get_logger()
        try:
            if towardsuserid is None:
                return UserInteractionSentiment.objects(
                    user_id=userid,
                    content_id=contentid).get()
            else:
                return UserInteractionSentiment.objects(
                    user_id=userid,
                    content_id=contentid,
                    towards_user=towardsuserid).get()
        except dbcontext.DoesNotExist:
            logger.debug(f"User does not exists {userid}  {contentid}")
        return None

    @staticmethod
    def add_if_not_exists(userid, content_type, contentid, towards_userid, sentiments):
        logger = ApiLogger.get_logger()
        logger.debug(f"Adding user if not exists")
        try:
            existing_interaction = UserInteractionSentiment.objects(
                user_id=userid,
                content_type=content_type,
                content_id=contentid).get()
            logger.debug(f"Found user {existing_interaction.toJson()}")
            return existing_interaction, ALREADY_EXISTS
        except dbcontext.DoesNotExist:
            logger.debug(f"user does not exist")
            pass

        logger.debug(f"user does not exist, creating it - userid {userid} ")
        user_interaction = UserInteractionSentiment(
            user_id=userid,
            content_type=content_type,
            content_id=contentid,
            towards_user=towards_userid,
            sentiments=sentiments)

        user_interaction.save()

        return user_interaction, NEW_ENTRY_ADDED

    def toJson(self):
        return f"user_id: {self.user_id} towards_user: {self.towards_user} content_type: {self.content_type} content_id: {self.content_id} sentiments: {self.sentiments}"
