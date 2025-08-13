# accounts/views.py
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm
from .forms import ProfileUpdateForm, CustomPasswordChangeForm, MultipleUserSettingsForm
from .models import CustomUser, UserSetting
from social.models import Post
from utils.notifications import create_notification
from utils.templatetags.rights import can_edit_post
from utils.settings import get_user_settings

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



def user_list(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(is_active=True).order_by('nickname')

    if query:
        users = users.filter(
            Q(nickname__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    posts_per_page = get_user_settings(['POSTS_PER_PAGE'], request.user).get('POSTS_PER_PAGE', 10)
    paginator = Paginator(users, posts_per_page)  # по 10 пользователей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'accounts/user_list.html',
        {'page_obj': page_obj, 'query': query}
    )


def public_profile(request, nickname):
    user_profile = get_object_or_404(User, nickname=nickname)
    posts = user_profile.posts.all()
    followers_count = user_profile.followers.count()
    following_count = user_profile.following.count()
    return render(request, 'accounts/public_profile.html', {
        'profile_user': user_profile,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
    })


@login_required
@require_POST
def toggle_follow(request, nickname):
    if request.user.nickname == nickname:
        return JsonResponse({'success': False, 'error': 'Нельзя подписаться на самого себя.'})

    try:
        target_user = get_object_or_404(CustomUser, nickname=nickname)
        print(f'Пользователь {target_user} найден. {request.user} {request.user.following.all()}')  # Добавляем эту строку для отладки (можно удалить, если не нужно)target_user)
    except:
        return JsonResponse({'success': False, 'error': 'Пользователь не найден.'})

    if target_user in request.user.following.all():
        request.user.following.remove(target_user)
        is_following = False
    else:
        request.user.following.add(target_user)
        create_notification(actor=request.user, recipient=target_user, verb='follow')
        is_following = True

    response = JsonResponse({'success': True, 'is_following': is_following})
    return response


def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_email_confirmed = True
        user.save()
        messages.success(request, 'Email подтвержден. Теперь вы можете пользоваться всеми функциями.')
    else:
        messages.error(request, 'Ссылка подтверждения недействительна или устарела.')

    return redirect('accounts:login')


@login_required
def resend_activation_email(request):
    user = request.user
    if user.is_email_confirmed:
        messages.info(request, 'Email уже подтвержден.')
        return redirect('accounts:profile')

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = request.build_absolute_uri(
        reverse('accounts:confirm_email', kwargs={'uidb64': uid, 'token': token})
    )

    subject = 'Подтверждение Email'
    message = render_to_string('accounts/email_confirmation_email.html', {
        'user': user,
        'activation_link': activation_link,
    })

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    messages.success(request, 'Письмо с подтверждением отправлено на вашу почту.')
    return redirect('accounts:profile')

@login_required
def edit_user_settings(request):
    current_values = get_user_settings(['CHAT_REFRESH_INTERVAL', 'POSTS_PER_PAGE'], request.user)
    if request.method == 'POST':
        form = MultipleUserSettingsForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, "Настройки сохранены")
            return redirect('accounts:edit_user_settings')
    else:
        form = MultipleUserSettingsForm(initial={
            'chat_refresh_interval': current_values['CHAT_REFRESH_INTERVAL'],
            'posts_per_page': current_values['POSTS_PER_PAGE'],
        })
    return render(request, 'accounts/edit_user_settings.html', {'form': form})
