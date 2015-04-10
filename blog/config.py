import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgres://jakauqgzidtdtx:VcXGQjs7H7EnbqnnFrFQTN_cGj@ec2-54-163-226-9.compute-1.amazonaws.com:5432/d79fao3btq7b6k"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "99problemsbutascootsaintone")