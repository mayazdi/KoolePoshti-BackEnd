from .post import PostApi


def initialize_routes(api):
    api.add_resource(PostApi, '/post')
