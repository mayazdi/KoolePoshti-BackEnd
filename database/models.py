from .db import db
import datetime

class Avatar(db.Document):
    data = db.ImageField()


class File(db.Document):
    name = db.StringField()
    size = db.IntField()
    # url = db.StringField(required=True)
    data = db.FileField()


class User(db.Document):
    githubId = db.StringField()
    beheshtiEmail = db.EmailField(required=True, unique=True)
    # activation_token = db.StringField()
    active = db.BooleanField(required=True, default=False)
    password = db.StringField(required=True)
    otp_valid_date = db.DateTimeField(required=True, default=datetime.datetime.utcnow() + datetime.timedelta(days=1))
    otp = db.StringField(required=True)
    firstName = db.StringField(required=True)
    lastName = db.StringField(required=True)
    avatar = db.ReferenceField(Avatar)


class Category(db.Document):
    title = db.StringField(required=True)


class Tag(db.Document):
    name = db.StringField(required=True)
    color = db.StringField(max_length=6, min_length=6)
    category = db.ReferenceField(Category)


class Like(db.Document):
    pass


class Post(db.Document):
    # _id = db.IntField(required=True, unique=True)
    active = db.BooleanField(required=True, default=True)
    createdAt = db.DateTimeField(required=True, default=datetime.datetime.utcnow)
    # Change this to author
    user = db.ReferenceField(User, required=True)
    content = db.StringField(required=True)
    likes = db.ListField(db.ReferenceField(User))
    file = db.ListField(db.ReferenceField(File))

    meta = {'allow_inheritance': True}


class Comment(db.Document):
    content = db.StringField(required=True)
    # Change this to author
    user = db.ReferenceField(User, required=True)
    post = db.ReferenceField(Post, required=True)


class GHPost(Post):
    forks = db.IntField(required=True)
    stars = db.IntField(required=True)
    url = db.IntField(required=True)
    metaPicture = db.StringField(required=True)
    metaTitle = db.StringField(required=True)
    metaDescription = db.StringField()
