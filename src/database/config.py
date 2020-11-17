import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

class Connection:
    """ Connection class handle with app configuration and
        database connections.
    """
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.return_url()
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'admin')
        self.db = SQLAlchemy(self.app)
        self.migrate = Migrate(self.app, self.db)
        self.manager = Manager(self.app)
        self.manager.add_command('db', MigrateCommand)
    
    def return_url(self):
        url = 'mysql+pymysql://' + \
            os.environ.get('MYSQL_USER', 'invalid') + ':' + \
            os.environ.get('MYSQL_PASS', 'invalid') + '@' + \
            os.environ.get('MYSQL_HOST',
                        'invalid') \
                        + ':' + \
            os.environ.get('MYSQL_PORT', 'invalid') + '/' + \
            os.environ.get('MYSQL_DATABASE', 'invalid')
            
        return url
