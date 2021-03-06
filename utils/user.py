from database.models import User, Post, Comment

def get_user_id(email):
    user = User.objects.get(beheshtiEmail=email)
    return user.id

def is_post_author(email, post_id):
    post = Post.objects.get(id=post_id)
    post_author = post.author
    user_id = get_user_id(email)
    return post_author.id == user_id

def is_comment_author(email, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment_author = comment['author']
    user_id = get_user_id(email)
    return comment_author.id == user_id

