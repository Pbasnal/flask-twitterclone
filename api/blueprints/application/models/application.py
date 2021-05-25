import json

from api.models.MongoEngine import dbcontext
from logging_setup.logger import ApiLogger

RESPOND_WITH_NEW_ENTRY_ADDED = True
RESPOND_WITH_ALREADY_EXISTS = False


class Application(dbcontext.Document):

    application_name = dbcontext.StringField(required=True, max_length=50)
    application_id = dbcontext.StringField(required=True)
    application_secret = dbcontext.StringField(required=True)

    # Token is generated and is used for subsequent calls
    # this is to maintain and open sessions with applications
    # during which multiple requests can be made to the API
    # todo: Subject to changes
    application_token = dbcontext.StringField(required=False)
    token_expiration = dbcontext.DateTimeField(required=False)

    @staticmethod
    def get_application_for_token(token: str):
        FLOW_ID = "GET_APPLICATION_DETAILS"
        if token is None or token.strip() == "":
            ApiLogger.log_debug(FLOW_ID, "FAILED_INPUT",
                                f"No token provided ({token})")
            return None
        try:
            app = Application.objects(application_token=token).get_or_404()
            ApiLogger.log_debug(FLOW_ID, "APPLICATION_DETAILS",
                                f"Application found ({app.application_id})")
            return app

        except dbcontext.DoesNotExist:
            ApiLogger.log_exception(FLOW_ID, "EXCEPTION",
                                    f"Token does not exists ({token})")

        return None

    @staticmethod
    def get(application_id: str):
        FLOW_ID = "GET_APPLICATION_DETAILS"
        if application_id is None or application_id.strip() == "":
            ApiLogger.log_debug(FLOW_ID, "FAILED_INPUT",
                                f"No application id provided ({application_id})")
            return None
        try:
            app = Application.objects().get_or_404(application_id=application_id)
            ApiLogger.log_debug(FLOW_ID, "APPLICATION_DETAILS",
                                f"Application found ({application_id})")
            return app

        except dbcontext.DoesNotExist:
            ApiLogger.log_exception(FLOW_ID, "EXCEPTION",
                                    f"Application does not exists ({application_id})")

        return None

    @staticmethod
    def add_new_application(application_name: str, application_id: str, application_secret: str) -> bool:
        FLOW_ID = "add_new_application".upper()
        ApiLogger.log_debug(FLOW_ID, "INPUT_ARGS", f"{{ \
            application_id: {application_id}, \
            application_secret: {application_secret}}}")

        try:
            app = Application.objects(application_id=application_id).get()
            ApiLogger.log_debug(
                FLOW_ID, "APPLICATION_ALREADY_EXISTS", repr(app))
            return RESPOND_WITH_ALREADY_EXISTS
        except dbcontext.DoesNotExist:
            ApiLogger.log_debug(FLOW_ID, "EXISTING_APPLICATION_NOT_FOUND", "")

        ApiLogger.log_debug(FLOW_ID, "INSERTING_NEW_APPLICATION", f"{{ \
            application_id: {application_id}, \
            application_secret: {application_secret}}}")

        app = Application(
            application_name=application_name,
            application_id=application_id,
            application_secret=application_secret)

        app.save()

        return RESPOND_WITH_NEW_ENTRY_ADDED
    
    @staticmethod
    def update_token(application_details) -> bool:
        FLOW_ID = "update_token".upper()
        ApiLogger.log_debug(FLOW_ID, "INPUT_ARGS", f"{{ \
            token: {application_details.application_token}, \
            token_expiration: {application_details.token_expiration}}}")

        try:
            application_details.save()
            ApiLogger.log_debug(
                FLOW_ID, "TOKEN_ADDED", repr(application_details))
            return application_details
        except:
            ApiLogger.log_exception(FLOW_ID, "FAILED_TO_UPDATE_TOKEN", "")

        return None

    def toJsonString(self):
        return f"""{{
    "user_id": {self.user_id},
    "towards_user": {self.towards_user},
    "content_type": {self.content_type},
    "content_id": {self.content_id},
    "sentiments": {self.sentiments}"
}}
"""
