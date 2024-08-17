from django.urls import path
from .views import UserListView, UserDetailView, GroupListView, GroupDetailView,index, SearchView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('', index, name='index'),
    path('search/', SearchView.as_view(), name='search'),
]