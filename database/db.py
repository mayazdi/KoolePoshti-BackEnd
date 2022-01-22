from flask_mongoengine import MongoEngine
from mongoengine import connect
from config import config_map

db = MongoEngine()

def initialize_db(app):
    db.init_app(app)

def clean_db():
    db = connect(config_map['mongodb_name'])
    db.drop_database(config_map['mongodb_name'])
    print('Dtabase cleaned successfully')

def initialize_categories():
    # Default categories will be initialized here
    pass

def initialize_tags():
    # Default tags will be initialized here
    pass

def repopulater_tags():
    pass