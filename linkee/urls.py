from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),
]