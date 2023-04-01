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
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('following_posts/', views.following_posts, name='following_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
]

