import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgres://hpulpkzdcudodr:c-hkq21sRJJ2fmujfAP7w5oT5I@ec2-54-197-238-8.compute-1.amazonaws.com:5432/dc1p7pp3qag615"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "99problemsbutascootsaintone")