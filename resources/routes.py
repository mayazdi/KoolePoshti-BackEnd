from .post import PostApi, PostsApi
from .comment import CommentApi, CommentsApi
from .main import MainApi, TermsApi

def initialize_routes(api, routing_prefix):
    api.add_resource(PostApi, routing_prefix + '/posts/<id>')
    api.add_resource(PostsApi, routing_prefix + '/posts')
    api.add_resource(CommentsApi, routing_prefix + '/posts/<id>/comments')
    api.add_resource(CommentApi, routing_prefix + '/posts/<id>/comments/<comment_id>')
    api.add_resource(MainApi, routing_prefix + '/')
    api.add_resource(TermsApi, routing_prefix + '/terms')
