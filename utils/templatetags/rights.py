from django import template
from datetime import timedelta
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
    return post.created_at >= timezone.now() - timedelta(days=7)
