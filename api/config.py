class Config():
    DEBUG = False
    TESTING = False

class Debug(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db':    'project1',
        'host':  'localhost',
        'port':  27017,
        'alias': 'default'
    }
    SECRET_KEY = "flask_secret_key"
    LOG_FILE = "logs/sentiment_api.log"
    WATSON_IAMAUTH_KEY = '6Fvsyz-UEoiceuciGxspHs2wP9rFZwUMgAG6izx-MKJX'
    WATSON_TONE_INSTANCE = "44e7bf19-e4b1-4b79-b9eb-d0d81e16fa7b"
    IAM = 'UXkI18-_VBdL2NpgI68psYDh9HWI3c7Ys8e3EPub9d7T'
