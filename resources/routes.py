from .post import PostApi, PostsApi
from .comment import CommentApi, CommentsApi
from .file import FileApi, FilesApi, FileDownloadApi, AvatarApi, AvatarsApi
from .tag import TagApi, CategoryApi
from .like import LikeApi, UnLikeApi
from .main import MainApi, TermsApi, OGApi
from .auth import SigninApi, SignupApi, ForgotApi, ActivateApi

def initialize_routes(api, routing_prefix):
    api.add_resource(PostApi, routing_prefix + '/posts/<id>')
    api.add_resource(PostsApi, routing_prefix + '/posts')
    api.add_resource(CommentsApi, routing_prefix + '/posts/<id>/comments')
    api.add_resource(CommentApi, routing_prefix + '/posts/<id>/comments/<comment_id>')
    api.add_resource(MainApi, routing_prefix + '/')
    api.add_resource(TermsApi, routing_prefix + '/terms')
    api.add_resource(AvatarApi, routing_prefix + '/avatars')
    api.add_resource(AvatarsApi, routing_prefix + '/avatars/<id>')
    api.add_resource(FileApi, routing_prefix + '/files')
    api.add_resource(FilesApi, routing_prefix + '/files/<id>')
    api.add_resource(FileDownloadApi, routing_prefix + '/files/<id>/download')
    api.add_resource(TagApi, routing_prefix + '/tag')
    api.add_resource(CategoryApi, routing_prefix + '/category')
    api.add_resource(OGApi, routing_prefix + '/og/<user>/<repository>')
    api.add_resource(LikeApi, routing_prefix + '/posts/<id>/like')
    api.add_resource(UnLikeApi, routing_prefix + '/posts/<id>/unlike')
    api.add_resource(SigninApi, routing_prefix + '/auth/signin')
    api.add_resource(SignupApi, routing_prefix + '/auth/signup')
    api.add_resource(ForgotApi, routing_prefix + '/auth/forgot')
    api.add_resource(ActivateApi, routing_prefix + '/auth/activate')

