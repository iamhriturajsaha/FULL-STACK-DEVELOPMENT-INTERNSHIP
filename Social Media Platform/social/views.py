from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Post, Profile, Follow, Notification, Comment, Like
from .forms import ProfileEditForm, PostForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

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

@login_required
def home_view(request):
    # For now, just show all posts
    posts = Post.objects.all().select_related('author__profile')
    return render(request, 'home.html', {'posts': posts})

def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = user_profile.posts.all()
    is_following = False
    if request.user.is_authenticated:
        is_following = user_profile.followers.filter(follower=request.user).exists()
        
    return render(request, 'profile.html', {
        'profile_user': user_profile,
        'posts': posts,
        'is_following': is_following
    })

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def toggle_follow(request, username):
    if request.method == 'POST':
        target_user = get_object_or_404(User, username=username)
        if target_user == request.user:
            return JsonResponse({'error': 'Cannot follow yourself'}, status=400)
            
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
        
        if not created:
            follow.delete()
            is_following = False
        else:
            is_following = True
            Notification.objects.create(
                recipient=target_user,
                actor=request.user,
                notification_type='follow'
            )
            
        return JsonResponse({
            'status': 'success',
            'is_following': is_following,
            'follower_count': target_user.followers.count()
        })
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('profile', username=request.user.username)

@login_required
def explore_view(request):
    posts = Post.objects.all().order_by('?')[:30]
    return render(request, 'explore.html', {'posts': posts})

@login_required
def search_view(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(username__icontains=query)[:5]
        user_results = [{'username': u.username, 'avatar': u.profile.avatar.url if u.profile.avatar else None} for u in users]
        return JsonResponse({'status': 'success', 'users': user_results})
    return JsonResponse({'status': 'success', 'users': []})

@login_required
def toggle_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            is_liked = False
        else:
            is_liked = True
            if request.user != post.author:
                Notification.objects.create(recipient=post.author, actor=request.user, notification_type='like', post=post)
        return JsonResponse({'status': 'success', 'is_liked': is_liked, 'like_count': post.likes.count()})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        if content:
            post = get_object_or_404(Post, id=post_id)
            comment = Comment.objects.create(post=post, author=request.user, content=content)
            if request.user != post.author:
                Notification.objects.create(recipient=post.author, actor=request.user, notification_type='comment', post=post)
            return JsonResponse({
                'status': 'success', 
                'comment_id': comment.id, 
                'author': comment.author.username, 
                'content': comment.content, 
                'created_at': comment.created_at.strftime('%B %d, %Y')
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)
