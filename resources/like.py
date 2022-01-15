from flask import Response, request
from database.models import Post
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.user import get_user_id
from mongoengine.queryset.visitor import Q

class LikeApi(Resource):
    decorators = [jwt_required()]

    def post(self, id):
        user_id = get_user_id(get_jwt_identity())
        post = Post.objects.get(id=id)
        for u in post.likes:
            if user_id == u.id:
                return {'msg': 'already liked'}, 200
        post.likes.append(user_id)
        post.save()
        return {'msg': 'post liked'}, 201


class UnLikeApi(Resource):
    decorators = [jwt_required()]
    
    def post(self, id):    
        user_id = get_user_id(get_jwt_identity())
        post = Post.objects.get(id=id)
        new_likes = []
        user_liked = False
        for u in post.likes:
            if user_id != u.id:
                new_likes.append(u)
            else:
                user_liked = True
        if user_liked:
            post.likes = new_likes
            post.save()
            return {'msg': 'post unliked'}, 201
        else:
            return {'msg': 'post was not liked'}, 200