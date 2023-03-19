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
]

