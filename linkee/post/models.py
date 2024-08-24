from django.db import models

from user.models import LinkeeUser

class Post(models.Model):
    user = models.ForeignKey(LinkeeUser, on_delete=models.CASCADE)
    postContent = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(LinkeeUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'post')

class Comment(models.Model):
    user = models.ForeignKey(LinkeeUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentContent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)