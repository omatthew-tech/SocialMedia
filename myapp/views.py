from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Post, Comment, Like, Follow, Vote
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import ProfileForm
from .models import Profile

from .models import FriendRequest

from .models import Follow, FriendRequest

from django.contrib.auth.models import User
from .models import Follow



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    posts = Post.objects.all()
    post_form = PostForm()
    following_users = [follow.followed_user for follow in request.user.following.all()]
    comment_form = CommentForm()
    post_likes = {post.id: post.like_count() for post in posts}
    return render(request, 'home.html', {'posts': posts, 'post_form': post_form, 'comment_form': comment_form, 'post_likes': post_likes, 'following_users': following_users})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def create_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('home')

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    like = Like.objects.filter(post=post, user=request.user).first()
    if like:
        like.delete()
    else:
        like = Like(post=post, user=request.user)
        like.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def vote_post(request, post_id):
    post = Post.objects.get(id=post_id)
    vote = Vote.objects.filter(post=post, user=request.user).first()
    if vote:
        vote.delete()
    else:
        vote = Vote(post=post, user=request.user)
        vote.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@user_passes_test(lambda user: not user.is_authenticated, login_url='home', redirect_field_name=None)
def landing(request):
    return render(request, 'landing.html')



# views.py
from django.contrib.auth.decorators import login_required

@login_required
def following_posts(request):
    followed_users = request.user.following.values_list('followed_user', flat=True)
    posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')
    return render(request, 'following_posts.html', {'posts': posts})



def profile(request, username):
    user = get_object_or_404(User, username=username)
    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(user=request.user, followed_user=user).exists()

    return render(request, 'profile.html', {'user': user, 'is_following': is_following})


@login_required
def edit_profile(request):
    user = request.user
    user_profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def requests(request):
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'requests.html', {'friend_requests': friend_requests})

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    from_user_profile = Profile.objects.get(user=friend_request.from_user)
    to_user_profile = Profile.objects.get(user=friend_request.to_user)
    from_user_profile.friends.add(to_user_profile)
    to_user_profile.friends.add(from_user_profile)
    friend_request.delete()
    return redirect('requests')



@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    follow, created = Follow.objects.get_or_create(user=request.user, followed_user=user_to_follow)
    if not created:
        follow.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    try:
        follow = Follow.objects.get(user=request.user, followed_user=user_to_unfollow)
        follow.delete()
    except Follow.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    if not created:
        friend_request.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

