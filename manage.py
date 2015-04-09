import os
from flask.ext.script import Manager
from blog.models import Post
from blog.database import session

from blog import app

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
@manager.command
def seed():
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing..."""
    
    for i in range(25):
        post = Post(
            title="Test Post #{}".format(i),
            content=content
        )
        session.add(post)
    session.commit()

if __name__ == "__main__":
    manager.run()