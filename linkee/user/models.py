from django.db import models
from django.contrib.auth.models import AbstractUser, get_user_model

class LinkeeUser(AbstractUser):
    address = models.CharField(max_length=255, blank=True, null=True)
    uni_name = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(LinkeeUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Friend(models.Model):
    user = models.ForeignKey(LinkeeUser, on_delete=models.CASCADE, related_name='friend_requests_sent')
    friend = models.ForeignKey(LinkeeUser, on_delete=models.CASCADE, related_name='friend_requests_received')
    friend_status = models.CharField(max_length=50, choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Blocked', 'Blocked'), ('Pending', 'Pending')], default='Pending')

    class Meta:
        unique_together = ('user', 'friend')
        


User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'
