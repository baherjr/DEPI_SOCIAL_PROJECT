from django.urls import path
from . import views

urlpatterns = [
    path('view_my_posts/',view=views.view_my_posts, name="myposts"),
    path('view_feed/', view=views.view_feed,name="view_feed"),
    path('create_post/', views.create_post, name='create_post'),
    path('add_like/<int:post_id>/', views.add_like, name='add_like'),
    path('post/<int:post_id>/comments/', views.view_comments, name='view_comments'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
]