#import logging
import sys
from loguru import logger as Log

## Method to initialize logger
class ApiLogger():
    __instance = None

    @staticmethod 
    def get_logger(filepath=None):
        
        """ Static access method. """
        if filepath is not None and ApiLogger.__instance is None:
            ApiLogger(filepath)
            Log.info("Initializing logger")
        
        print("Just prinint")
        Log.info("Reusing logger")
        return ApiLogger.__instance.logger

    @staticmethod
    def log_debug(flow_id, event_id, message):
        print(f"{flow_id} | {event_id} > {message}")
        ApiLogger.__instance.logger.debug(f"{flow_id} | {event_id} > {message}")

    @staticmethod
    def log_exception(flow_id, event_id, message):
        print(f"{flow_id} | {event_id} > {message}")
        ApiLogger.__instance.logger.exception(f"{flow_id} | {event_id} > {message}")

    def __init__(self, filepath):
        
        """ Virtually private constructor. """
        if ApiLogger.__instance != None:
            ApiLogger.__instance.logger.debug(
                "API_SETUP", "LOGGER_ALREADY_INITIALIZED",
                "This class is a singleton!")
            return
        
        ApiLogger.__instance = self
        ## loguru setup
        self.logger = Log

        self.logger.add(sys.stderr, format="{time} {message}")
        self.logger.add(sys.stdout, format="{time} {message}")
        self.logger.add(filepath, rotation="500 MB")


        ## old setup =>

        #self.logger = None
        # logging.basicConfig(filename=filepath,
        #                             format='%(asctime)s %(message)s',
        #                             filemode='w')

        # self.logger = logging.getLogger()
        # self.logger.setLevel(logging.DEBUG)
    

## Decorator approach is good, but figure out how to use FLOW_ID
## and event id with this.
## Additionally, if the decorator can be used to keep track of the execution
## then we can have CorelationVector as well.

# def log_arguments_and_return(method):
#     def wrapper():
#         ApiLogger.log_debug(method.__name__)
#         result = method()

#         return result
#     return wrapper