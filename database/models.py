from .db import db

class User(db.Document):
    github_id = db.StringField(required=True)
    beheshti_id = db.StringField()
    first_name = db.StringField()
    last_name = db.StringField()
    avatar_url = db.StringField()
    phone_number = db.IntField()


class Tag(db.Document):
    # hash
    pass


class File(db.Document):
    url = db.StringField(required=True)


class Post(db.Document):
    _id = db.IntField(required=True, unique=True)
    active = db.BooleanField(required=True)
    created_at = db.DateTimeField(required=True)
    likes = db.ReferenceField(User)
    content = db.StringField()
    tags = db.ListField(db.ReferenceField(Tag))
    _file = db.ListField(db.ReferenceField(File))

    meta = {'allow_inheritance': True}


class GHPost(Post):
    forks = db.IntField(required=True)
    stars = db.IntField(required=True)
    link = db.IntField(required=True)
    meta_picture = db.StringField(required=True)
    meta_title = db.StringField(required=True)
    meta_description = db.StringField()