import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY")
    MAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")