from django.urls import path
from . import views

# urlpatterns = [
#     path('',login,name="login"),
#     path('register/', view=register,name="register"),
#     path('user_profile/', view= user_profile, name="home"),
#     path('logout/', view=logout, name='logout'),
# ]

urlpatterns = [
    path('',view=views.login, name="login"),
    path('register/',view=views.register, name="register"),
    path('linkee/',view=views.home_page,name='linkee'),
    path('logout/',view=views.logout,name="logout"),
    path('profile/', view=views.profile_page, name="profile"),
    path('friend_requests/',view=views.friend_requests, name="friend_requests"),
    path('friends/',view=views.view_friends, name="view_friends"),
    path('get_friend_count/',view=views.get_friend_count, name="friend_count"),
    path('post/<int:post_id>/comments/', views.view_comments, name='view_comments'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    # path('handle_friend_request/', views.handle_friend_request, name="handle_friend_request"),
    path('handle_friend_request/<str:request_friend_id>/<str:action>/', views.handle_friend_request, name="handle_friend_request"),
    # 'handle_friend_request/<str:request_username>/<str:action>/'
]