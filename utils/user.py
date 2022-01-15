from database.models import User, Post

def get_user_id(email):
    user = User.objects.get(beheshtiEmail=email)
    return user.id

def is_post_author(email, post_id):
    post = Post.objects.get(id=post_id)
    # change user to author
    post_author = post.user
    user_id = get_user_id(email)
    return post_author.id == user_id

