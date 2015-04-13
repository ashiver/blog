import os
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
mail = Mail(app)
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig")
app.config.from_object(config_path)



from . import views
from . import filters
from . import login