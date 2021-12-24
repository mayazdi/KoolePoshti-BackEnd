from flask import Response, request
from database.models import Post
from flask_restful import Resource

class PostApi(Resource):
    def get(self, id):
        post = Post.objects.get(id=id).to_json()
        if post:
            status_code = 200
        else:
            status_code = 404
        return Response(post, mimetype='application/json', status=status_code)
    
    def put(self, id):
        body = request.get_json()
        Post.objects.get(id=id).update(**body)
        return '', 200

    def delete(self, id):
        Post.objects.get(id=id).delete()
        return '', 200


class PostsApi(Resource):
    def get(self):
        page = request.args.get("page")
        limit = request.args.get("limit")
        if page and limit:
            page = (int) (page)
            limit = (int) (limit)
            start_index = (page - 1) * limit
            end_index = page * limit
            posts = Post.objects[start_index:end_index].to_json()
            # If has_next, ... is needed, get it from paginate file
        else:
            posts = Post.objects().to_json()
        return Response(posts, mimetype="application/json", status=200)
    
    def post(self):
        body = request.get_json()
        post = Post(**body).save()
        id = post.id
        return {'id': str(id)}, 201
