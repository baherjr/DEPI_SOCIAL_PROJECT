from django.contrib import admin
from .models import CustomUser, Post

admin.site.register(CustomUser)
admin.site.register(Post)
