from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib

class User(AbstractUser):
    email = models.EmailField(unique=True)
    Fname = models.CharField(max_length=20, null=False)
    Lname = models.CharField(max_length=20, null=False)
    job = models.CharField(max_length=100, null=True, blank=True)  # Set blank=True for optional fields
    UniName = models.CharField(max_length=100, null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['Fname', 'Lname']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Use built-in fields for better compatibility

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True, null=True)
    profile_picture_url = models.URLField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user}"

class Friendship(models.Model):
    user = models.ForeignKey(
        User,
        related_name='friendship_set',
        on_delete=models.CASCADE
    )
    friend = models.ForeignKey(
        User,
        related_name='friend_set',
        on_delete=models.CASCADE
    )
    friend_status = models.CharField(
        max_length=50,
        choices=[
            ('Accepted', 'Accepted'),
            ('Rejected', 'Rejected'),
            ('Blocked', 'Blocked'),
            ('Pending', 'Pending'),
        ],
        default='Pending'
    )

    class Meta:
        unique_together = ('user', 'friend')
        constraints = [
            models.UniqueConstraint(fields=['user', 'friend'], name='unique_friendship')
        ]

    def __str__(self):
        return f"{self.user} - {self.friend} ({self.friend_status})"
