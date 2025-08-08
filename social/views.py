#social/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .forms import PostForm, CommentForm
from .models import Post,  Comment

from utils.notifications import create_notification
from utils.templatetags.rights import can_edit_post, can_delete_comment, can_delete_post



@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('social:post_list')
    return render(request, 'social/post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user or not can_edit_post(post, request.user):
        return redirect('social:post_list')

    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('social:post_list')
    return render(request, 'social/post_form.html', {'form': form, 'edit': True, 'post': post})

#@login_required
def post_list(request):
    posts = Post.objects.select_related('author').prefetch_related('comments', 'likes')
    if request.user.is_authenticated:
        filter_type = request.GET.get('filter')
        if filter_type == 'following':
            posts = posts.filter(author__in=request.user.following.all())
        elif filter_type == 'not_following':
            posts = posts.exclude(Q(author__in=request.user.following.all()) | Q(author=request.user))
        elif filter_type == 'followers':
            posts = posts.filter(author__in=request.user.followers.all())

    posts = posts.order_by('-created_at')
    paginator = Paginator(posts, 10)  # по 10 пользователей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'social/post_list.html', {'page_obj': page_obj})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.select_related('author')
    form = CommentForm(request.POST or None)
    paginator = Paginator(comments, 10)  # по 10 пользователей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        create_notification(actor=request.user, recipient=post.author, verb='comment', target=comment)
        return redirect('social:post_detail', pk=pk)
    return render(request, 'social/post_detail.html', {
        'post': post,
        'page_obj': page_obj,
        'form': form
    })

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not can_delete_post(post,request.user):
        messages.error(request, "Вы не можете удалить этот пост.")
        return redirect('social:post_edit', pk=post.id)

    post.delete()
    messages.success(request, "Пост успешно удалён.")
    return redirect('social:post_list')

@login_required
def post_like_toggle(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
        create_notification(actor=user, recipient=post.author, verb='like', target=post)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count(),
        })

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)
    # post = get_object_or_404(Post, pk=pk)
    # if request.user in post.likes.all():
    #     post.likes.remove(request.user)
    # else:
    #     post.likes.add(request.user)
    # next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    # return redirect(next_url)
    # # return HttpResponseRedirect(reverse('social:post_detail', args=[pk]))

# @login_required
# def comment_add(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     print(post)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.post = post
#             comment.save()
#             print(comment)
#             create_notification(actor=request.user, recipient=post.author, verb='comment', target=comment)
#     return redirect('social:post_detail', pk=post.id)

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if not can_delete_comment(comment, request.user):
        messages.error(request, "Вы не можете удалить этот комментарий.")
        return redirect('social:post_detail', pk=comment.post.id)

    comment.delete()
    messages.success(request, "Комментарий удалён.")
    return redirect('social:post_detail', pk=comment.post.id)

@login_required
def notification_list(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'social/notifications.html', {'notifications': notifications})
