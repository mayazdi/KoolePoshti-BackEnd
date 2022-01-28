from flask import Response, request
from database.models import Post, User, Comment
from flask_restful import Resource
from mongoengine.queryset.visitor import Q
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.user import get_user_id, is_post_author
from utils.github import get_repository_information
import re

#  ---------------------- UTIL FUNCTIONS ----------------------
def get_user(user):
    return {
        "id": str(user.id),
        "githubId": user.githubId,
        "beheshtiEmail": user.beheshtiEmail,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "avatar": user.avatar
    }

def get_comment(comment):
    return {
        "id" : str(comment.id),
        "content" : comment.content,
        "author" : get_user(comment.author),
    }

def get_comments(post_id):
    comments = Comment.objects(Q(post=post_id))
    cmnts = []
    for comment in comments:
        cmnts.append(get_comment(comment))
    return cmnts


def get_tag(tag):
    return {
        "id" : str(tag.id),
        "name" : tag.name,
        "color" : tag.color
    }

def get_tags(tags):
    tgs = []
    for tag in tags:
        tgs.append(get_tag(tag))
    return tgs

def get_file(f):
    return {
        "id" : str(f.id),
        "name" : f.name,
        "size" : f.size
    }

def get_files(files):
    fls = []
    for f in files:
        fls.append(get_file(f))
    return fls

def get_ghpost(post):
    url = {"repoUrl" : post['repoUrl']}
    ghpost_info = get_repository_information(post['repoUrl'])
    post = get_post(post)
    post = {**post , **ghpost_info, **url}
    return post

def get_comments_count_from_post_id(post_id):
    return Comment.objects(Q(post=post_id)).count()

def get_post(post):
    post = {
        "id" : str(post.id),
        "createdAt" : post.createdAt.strftime('%s'),
        "content" : post.content,
        "author" : get_user(post.author),
        "tags" : get_tags(post.tags),
        "files" : get_files(post.files),
        "comments" : get_comments_count_from_post_id(str(post.id)),
        "likes" : len(post.likes),
    }
    return post

def get_posts(posts):
    psts = []
    for post in posts:
        if 'repoUrl' in post:
            psts.append(get_ghpost(post))
        else:
            psts.append(get_post(post))
    return psts

#  ---------------------- UTIL FUNCTIONS ----------------------

class PostApi(Resource):
    decorators = [jwt_required()]

    def get(self, id):
        post = Post.objects(Q(id=id) | Q(active=True))
        # post = Post.objects.get(id=id).to_json()
        if post:
            post = post[0]
            if post.repoUrl:
                post = get_ghpost(post)
            else:
                post = get_post(post)
            comments = {"comments" : get_comments(id)}
            post = {**post, **comments}
            print(post)
            # status_code = 200
        else:
            return {"Error" : "Item not found"}, 404
        return post, 200
        # return Response(post, mimetype='application/json', status=status_code)
        
    def put(self, id):
        try:
            post = Post.objects.with_id(id)
            if post:
                if is_post_author(get_jwt_identity(), id):
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
                if is_post_author(get_jwt_identity(), id):
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
        tags = request.args.getlist("tags")
        query = Q(active=True)
        for t in tags:
            query = query & Q(tags=t)
        # print(query)
        if page and limit:
            page = (int) (page)
            limit = (int) (limit)
            start_index = (page - 1) * limit
            end_index = page * limit
        else:
            start_index = 0
            end_index = 20
        posts = get_posts(Post.objects(query)[start_index:end_index])
        return {
            "posts" : posts,
            "hasNext" : len(Post.objects(query)[end_index:end_index+1]) > 0
        }, 200
    
    def post(self): 
        user_id = get_user_id(get_jwt_identity())
        body = request.get_json()
        body['author'] = user_id
        if 'repoUrl' in body:
            if not re.match(r"^(http(s)?:\/\/)?(www.)?github\.com\/([\w\-\.]+)\/([\w\-\.]+)$", body['repoUrl']):
                return {"Error": "RepoUrl must be in github.com/user/repo format"}, 400
        post = Post(**body).save()
        id = post.id
        return {'id': str(id)}, 201
