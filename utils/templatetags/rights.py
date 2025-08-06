from django import template
from datetime import timedelta
from django.conf import settings
from django.utils import timezone

register = template.Library()


@register.filter
def is_owner(obj, user):
    """Проверка, является ли пользователь владельцем объекта"""
    return hasattr(obj, 'author') and obj.author == user


@register.filter
def has_admin_rights(user):
    """Проверка, является ли пользователь админом или суперпользователем"""
    return user.is_superuser or user.is_staff


@register.filter
def can_edit_post(post, user):
    """Может ли пользователь редактировать пост (например, в течение 7 дней)"""
    if not hasattr(post, 'author') or post.author != user:
        return False
    return post.created_at >= timezone.now() - timedelta(days=getattr(settings, 'POST_EDIT_DAYS', 7))

@register.filter
def can_delete_post(post, user):
    """Может ли пользователь удалить пост (например, в течение 30 дней)"""
    if not hasattr(post, 'author') or post.author != user:
        return False
    return post.created_at >= timezone.now() - timedelta(days=getattr(settings, 'POST_DELETE_DAYS', 7))


@register.filter
def can_delete_comment(comment, user):
    if comment.author != user:
        return False
    return timezone.now() - comment.created_at < timedelta(days=getattr(settings, 'COMMENT_DELETE_DAYS', 7))