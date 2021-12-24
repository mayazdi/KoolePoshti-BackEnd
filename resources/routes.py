from .post import PostApi, PostsApi
from .like import LikeApi, UnLikeApi


def initialize_routes(api, routing_prefix):
    api.add_resource(PostApi, routing_prefix + '/posts/<id>')
    api.add_resource(PostsApi, routing_prefix + '/posts')
    api.add_resource(LikeApi, routing_prefix + '/posts/<id>/like')
    api.add_resource(UnLikeApi, routing_prefix + '/posts/<id>/unlike')
