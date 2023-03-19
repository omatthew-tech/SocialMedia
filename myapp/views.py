from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Post, Comment, Like, Follow
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import user_passes_test

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
    comment_form = CommentForm()
    post_likes = {post.id: post.like_count() for post in posts}
    return render(request, 'home.html', {'posts': posts, 'post_form': post_form, 'comment_form': comment_form, 'post_likes': post_likes})


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
    return redirect('home')

@user_passes_test(lambda user: not user.is_authenticated, login_url='home', redirect_field_name=None)
def landing(request):
    return render(request, 'landing.html')
