from flask import Response, request
from database.models import Post
from flask_restful import Resource

class LikeApi(Resource):
    def post(self, id):
        """ body = request.get_json()
        post = Post(**body).save()
        id = post.id """
        return {'id': str(id)}, 201


class UnLikeApi(Resource):
    def post(self, id):
        """ body = request.get_json()
        post = Post(**body).save()
        id = post.id """
        return {'id': str(id)}, 201
