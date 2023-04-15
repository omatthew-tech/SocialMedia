from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('landing/', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', login_required(views.home), name='home'),
    path('create_post/', views.create_post, name='create_post'),
    path('create_comment/<int:post_id>/', views.create_comment, name='create_comment'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('vote_post/<int:post_id>/', views.vote_post, name='vote_post'),
    path('following_posts/', views.following_posts, name='following_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('requests/', views.requests, name='requests'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('send_friend_request/<str:username>/', views.send_friend_request, name='send_friend_request'),
]

