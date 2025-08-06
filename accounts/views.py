from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash

from .forms import CustomUserCreationForm
from .forms import ProfileUpdateForm, CustomPasswordChangeForm
from .models import CustomUser
from social.models import Post
from utils.templatetags.rights import can_edit_post

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('social:post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
    return render(request, 'accounts/logout_confirm.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('social:post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'posts': posts,
    })

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'accounts/password_change.html', {'form': form})

User = get_user_model()

def user_list(request):
    users = User.objects.filter(is_active=True).order_by('username')
    return render(request, 'accounts/user_list.html', {'users': users})

def public_profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = user_profile.posts.all()
    return render(request, 'accounts/public_profile.html', {
        'profile_user': user_profile,
        'posts': posts,
    })

@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user == target_user:
        return redirect('accounts:public_profile', username=username)

    if request.user.following.filter(id=target_user.id).exists():
        request.user.following.remove(target_user)
    else:
        request.user.following.add(target_user)

    return redirect('accounts:public_profile', username=username)
