from flask import Response, request
from database.models import Comment, Post
from flask_restful import Resource
from mongoengine.queryset.visitor import Q
from flask_jwt_extended import jwt_required

class CommentsApi(Resource):
    decorators = [jwt_required()]

    def get(self, id):
        comments = Comment.objects(post=id)
        # comments_count = len(comments)
        comments = comments.to_json()
        return Response(comments, mimetype="application/json", status=200)
    
    def post(self, id):
        body = request.get_json()
        comment = Comment(**body)
        post = Post.objects.get(id=id)
        comment.post = post
        comment.save()
        comment_id = comment.id
        return {'id': str(comment_id), 'post_id': id}, 201


class CommentApi(Resource):
    decorators = [jwt_required()]

    def delete(self, id, comment_id):
        comment = Comment.objects(Q(id=comment_id)| Q(post=id))
        if comment:
            comment.delete()
            return '', 200
        else:
            return '', 404