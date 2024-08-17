from django.urls import path
from .views import UserListView, UserDetailView, GroupListView, GroupDetailView,index, SearchView, CreateUserView, LoginView,CreateGroupView, AddUserToGroupView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('', index, name='index'),
    path('search/', SearchView.as_view(), name='search'),
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('create_group/', CreateGroupView.as_view(), name='create_group'),
    path('add_user_to_group/', AddUserToGroupView.as_view(), name='add_user_to_group'),
    
]
