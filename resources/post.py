from flask import Response, request
from database.models import Post
from flask_restful import Resource
from mongoengine.queryset.visitor import Q
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.user import get_user_id, has_access

class PostApi(Resource):
    decorators = [jwt_required()]

    def get(self, id):
        post = Post.objects(Q(id=id) | Q(active=True)).to_json()
        # post = Post.objects.get(id=id).to_json()
        if post:
            status_code = 200
        else:
            status_code = 404
        return Response(post, mimetype='application/json', status=status_code)
    
    def put(self, id):
        try:
            post = Post.objects.with_id(id)
            if post:
                if has_access(get_jwt_identity(), id):
                    body = request.get_json()
                    Post.objects.get(id=id).update(**body)
                    return {'msg': 'Post deleted'}, 200
                else:
                    return {'error': 'Access denied'}, 403
            else:
                return {'error': 'Post Not found'}, 404
        except:
            pass

    def delete(self, id):
        try:
            post = Post.objects.with_id(id)
            if post:
                if has_access(get_jwt_identity(), id):
                    post.delete()
                    return {'msg': 'Post deleted'}, 200
                else:
                    return {'error': 'Access denied'}, 403
            else:
                return {'error': 'Post Not found'}, 404
        except:
            pass

class PostsApi(Resource):
    decorators = [jwt_required()]
    
    def get(self):
        page = request.args.get("page")
        limit = request.args.get("limit")
        if page and limit:
            page = (int) (page)
            limit = (int) (limit)
            start_index = (page - 1) * limit
            end_index = page * limit
            posts = Post.objects(Q(active=True))[start_index:end_index].to_json()
            # If has_next, ... is needed, get it from paginate file
        else:
            posts = Post.objects().to_json()
        return Response(posts, mimetype="application/json", status=200)
    
    def post(self):        
        user_id = get_user_id(get_jwt_identity())
        body = request.get_json()
        body['user'] = user_id
        post = Post(**body).save()
        id = post.id
        return {'id': str(id)}, 201
