from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.UserProfileView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user_profile'),
    path('friends/', views.FriendListView.as_view({'get': 'list'}), name='friend_list'),
    path('friend-requests/', views.FriendRequestView.as_view({'post': 'create'}), name='friend_request'),
    path('users/', views.UserProfileView.as_view({'post': 'create'}), name='create_user'),
]
