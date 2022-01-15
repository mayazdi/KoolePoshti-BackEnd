from flask_mongoengine import MongoEngine

db = MongoEngine()


def initialize_db(app):
    db.init_app(app)

def clear_db():
    # Clear model collections
    pass

def initialize_categories():
    # Default categories will be initialized here
    pass

def initialize_tags():
    # Default tags will be initialized here
    pass
