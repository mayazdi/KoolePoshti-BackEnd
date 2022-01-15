from flask import Response, request
from database.models import Post
from flask_restful import Resource
from flask_jwt_extended import jwt_required

class LikeApi(Resource):
    decorators = [jwt_required()]

    def post(self, id):
        """ body = request.get_json()
        post = Post(**body).save()
        id = post.id """
        return {'id': str(id)}, 201


class UnLikeApi(Resource):
    decorators = [jwt_required()]
    
    def post(self, id):
        """ body = request.get_json()
        post = Post(**body).save()
        id = post.id """
        return {'id': str(id)}, 201