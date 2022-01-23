from database.models import Category, Tag
from mongoengine import connect
from config import config_map
from os import listdir
from os.path import isfile, join
from flask import Flask
from flask_mongoengine import MongoEngine
import hashlib


def connect_to_db():
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
            'host': config_map['mongodb_host']
        }
    db = MongoEngine()
    db.init_app(app)

def clean_db():
    selected_db = connect(config_map['mongodb_name'])
    selected_db.drop_database(config_map['mongodb_name'])
    print('Dtabase cleaned successfully')

def initialize_categories():
    # Default categories will be initialized here
    pass

def initialize_tags():
    # Default tags will be initialized here
    pass

def repopulater_tags():
    connect_to_db()
    tags_location = config_map['tags_location']
    onlyfiles = [f for f in listdir(tags_location) if isfile(join(tags_location, f))]
    onlytxtfiles = [t for t in onlyfiles if t.endswith(".txt")]
    for textfile in onlytxtfiles:
        textfile_withoutextention = textfile[:-4]
        category = None
        try:
            category = Category.objects.get(title=textfile_withoutextention)
        except:
            category = Category()
            category.title = textfile_withoutextention
            category.save()
        print(category.id)
        with open(join(tags_location, textfile)) as f:
            for line in f:
                try:
                    tag = Tag.objects.get(name=line)
                except:
                    tag = Tag()
                    tag.name = line
                    tag.color = hashlib.md5(line.encode()).hexdigest()[:6]
                    tag.category = category
                    tag.save()
                print(tag.id)

