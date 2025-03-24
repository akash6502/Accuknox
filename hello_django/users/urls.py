from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('users/', views.UserAPIView.as_view(), name='users'),
    path('friend-request/', views.FriendRequestCreateView.as_view(), name='friend-request-create'),
    path('pending-friend-request/', views.FriendRequestPendingView.as_view(), name='pending-friend-request'),
    path('friend-request/<int:pk>/accept/', views.FriendRequestAcceptView.as_view(), name='friend-request-accept'),
    path('friends/', views.FriendsView.as_view(), name='friends'),
]
