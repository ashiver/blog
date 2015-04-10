import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgres://wogrykqpgkbtcg:tiSV9G5dPrd9op-OvgsCrp5IpO@ec2-107-20-159-103.compute-1.amazonaws.com:5432/d7b0dda2r1ck1f"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "99problemsbutascootsaintone")