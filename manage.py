from app import create_app,db
from flask_script import Manager,Server
from app.models import User,Role,Comment
app = create_app('development')

manager = Manager(app)
manager.add_command('server',Server)








if __name__ == '__main__':
    manager.run()