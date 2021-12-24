from .post import PostApi, PostsApi
from .file import FileApi, FilesApi

def initialize_routes(api, routing_prefix):
    api.add_resource(PostApi, routing_prefix + '/posts/<id>')
    api.add_resource(PostsApi, routing_prefix + '/posts')
    api.add_resource(FileApi, routing_prefix + '/file')
    api.add_resource(FilesApi, routing_prefix + '/file/<id>')
