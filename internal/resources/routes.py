from .post import PostApi

def initialize_route(api):
    api.add_resource(PostApi, '/post')