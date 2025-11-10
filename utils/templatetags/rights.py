# utils/templatetags/rights.py
from __future__ import annotations
from functools import lru_cache
from typing import Optional, Iterable, Union, Sequence

from django import template
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.apps import apps

from accounts.models import (
    CustomUser,
    Department,
    Right,
    UserDepartmentRight,
    NotificationRole,
    DepartmentNotificationRecipient,
)

register = template.Library()
# from accounts.models import UserDepartmentRight, Right, Department
#
# register = template.Library()
#
#
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
    if not hasattr(post, 'author') or post.author != user  or not can_interact(user):
        return False
    return post.created_at >= timezone.now() - timedelta(days=getattr(settings, 'POST_EDIT_DAYS', 7))

@register.filter
def can_delete_post(post, user):
    """Может ли пользователь удалить пост (например, в течение 30 дней)"""
    if not hasattr(post, 'author') or post.author != user  or not can_interact(user):
        return False
    return post.created_at >= timezone.now() - timedelta(days=getattr(settings, 'POST_DELETE_DAYS', 7))


@register.filter
def can_delete_comment(comment, user):
    """Может ли пользователь удалить комментарий (например, в течение 7 дней)"""
    if comment.author != user or not can_interact(user):
        return False
    return timezone.now() - comment.created_at < timedelta(days=getattr(settings, 'COMMENT_DELETE_DAYS', 7))

@register.filter
def can_interact(user):
    """
    Проверка: можно ли пользователю взаимодействовать с контентом (лайкать, комментировать, публиковать).
    Включает подтверждение email, активность и т.д.
    """
    return getattr(user, 'is_fully_active', False)

@register.filter
def get_interaction_restriction_reason(user):
    if not getattr(user, 'is_active', False):
        return "Ваш аккаунт не активен."
    if not getattr(user, 'is_email_confirmed', False):
        return "Требуется подтверждение email."
    return ""

@register.filter
def has_any_right(user):
    try:
        return UserDepartmentRight.objects.filter(user=user).values_list("department", flat=True).exists()
    except:
        return False


# =============================
#    ВНУТРЕННИЕ ХЕЛПЕРЫ
# =============================

def _norm_dept_id(department_or_code: Union[int, str, Department, None]) -> Optional[int]:
    """Получить department_id из id / code / объекта Department. None -> None."""
    if department_or_code is None:
        return None
    if isinstance(department_or_code, int):
        return department_or_code
    if isinstance(department_or_code, Department):
        return department_or_code.id
    # строка = это code
    code = str(department_or_code).strip()
    if not code:
        return None
    return Department.objects.values_list("id", flat=True).filter(code__iexact=code).first()

@lru_cache(maxsize=512)
def _right_id_by_code(name: str) -> Optional[int]:
    if not name:
        return None
    return Right.objects.values_list("id", flat=True).filter(name__iexact=name).first()

@lru_cache(maxsize=512)
def _notif_role_id_by_code(name: str) -> Optional[int]:
    if not name:
        return None
    return NotificationRole.objects.values_list("id", flat=True).filter(name__iexact=name).first()

# =============================
#   ПУБЛИЧНЫЕ PY-ХЕЛПЕРЫ (для views и т.п.)
# =============================

# def has_dept_right(user: CustomUser,
#                    department_or_code: Union[int, str, Department, None],
#                    right_code: str = "") -> bool:
#     """
#     Если right_code пуст -> достаточно любого права в департаменте.
#     Иначе -> проверяем наличие конкретного права (name сравниваем __iexact).
#     """
#     if not user or not getattr(user, "is_authenticated", False):
#         return False
#
#     dep_id = _norm_dept_id(department_or_code)
#     if dep_id is None:
#         # Без департамента прав нет
#         return False
#
#     qs = UserDepartmentRight.objects.filter(user_id=user.id, department_id=dep_id)
#     if right_code:
#         rid = _right_id_by_code(right_code)
#         if not rid:
#             return False
#         qs = qs.filter(right_id=rid)
#     return qs.exists()
#
# def has_any_dept_rights(user: CustomUser,
#                         department_or_code: Union[int, str, Department, None],
#                         right_codes: Iterable[str]) -> bool:
#     if not user or not getattr(user, "is_authenticated", False):
#         return False
#     dep_id = _norm_dept_id(department_or_code)
#     if dep_id is None:
#         return False
#     right_ids = [r for r in (_right_id_by_code(c) for c in right_codes) if r]
#     if not right_ids:
#         return False
#     return UserDepartmentRight.objects.filter(
#         user_id=user.id, department_id=dep_id, right_id__in=right_ids
#     ).exists()

# def has_notif_role(user: CustomUser,
#                    department_or_code: Union[int, str, Department, None],
#                    notif_role_code: str) -> bool:
#     if not user or not getattr(user, "is_authenticated", False):
#         return False
#     dep_id = _norm_dept_id(department_or_code)
#     if dep_id is None:
#         return False
#     nrid = _notif_role_id_by_code(notif_role_code)
#     if not nrid:
#         return False
#     return DepartmentNotificationRecipient.objects.filter(
#         department_id=dep_id, role_id=nrid, user_id=user.id
#     ).exists()

# Новые функции обработки прав
def has_dept_right(department_or_code,
                   right_code: str,
                   user,
                   module: str = "requests",
                   **kwargs) -> bool:
    dept_id = _norm_dept_id(department_or_code)
    if not dept_id or not getattr(user, "has_corporate_access", False):
        return False
    module_code = (module or "requests").lower()
    if module_code == "finance":
        return _has_finance_right(dept_id, right_code, user, **kwargs)
    return UserDepartmentRight.objects.filter(
        user_id=user.id,
        department_id=dept_id,
        right__name__iexact=right_code,
        right__module__iexact=module_code,
    ).exists()

def has_any_dept_rights(department_or_code,
                        right_codes: Iterable[str],
                        user,
                        module: str = "requests",
                        **kwargs) -> bool:
    dept_id = _norm_dept_id(department_or_code)
    if not dept_id or not getattr(user, "has_corporate_access", False):
        return False
    module_code = (module or "requests").lower()
    if module_code == "finance":
        return _has_finance_any_rights(dept_id, right_codes, user, **kwargs)
    codes = [code for code in right_codes if code]
    if not codes:
        return False
    return UserDepartmentRight.objects.filter(
        user_id=user.id,
        department_id=dept_id,
        right__module__iexact=module_code,
        right__name__in=codes,
    ).exists()

def has_notif_role(department_or_code, role_code: str, user) -> bool:
    dept_id = _norm_dept_id(department_or_code)
    if not dept_id or not getattr(user, "has_corporate_access", False):
        return False
    return DepartmentNotificationRecipient.objects.filter(
        department_id=dept_id,
        role__name__iexact=role_code,
        user_id=user.id,
    ).exists()


# =============================
#  FINANCE-МОДУЛЬНЫЕ ПРАВА
# =============================

FINANCE_RIGHT_FIELD_MAP = {
    "budget_approver": "budget_approver",
    "approver": "budget_approver",
    "budget_coordinator": "budget_coordinator",
    "coordinator": "budget_coordinator",
    "request_preparer": "request_preparer",
    "preparer": "request_preparer",
}


def _get_finance_models():
    if not apps.is_installed("finance"):
        return None, None
    try:
        AccountingAccount = apps.get_model("finance", "AccountingAccount")
        DepartmentBudgetAccount = apps.get_model("finance", "DepartmentBudgetAccount")
    except LookupError:
        return None, None
    return AccountingAccount, DepartmentBudgetAccount


def _normalize_finance_account(account) -> Optional[int]:
    AccountingAccount, _ = _get_finance_models()
    if not AccountingAccount or account is None:
        return None
    if isinstance(account, int):
        return account
    if isinstance(account, AccountingAccount):
        return account.id
    if isinstance(account, str):
        account_number = account.strip()
    else:
        account_number = str(account).strip()
    if not account_number:
        return None
    return AccountingAccount.objects.filter(
        account_number__iexact=account_number
    ).values_list("id", flat=True).first()


def _resolve_finance_link(dept_id: int, **kwargs):
    AccountingAccount, DepartmentBudgetAccount = _get_finance_models()
    if not DepartmentBudgetAccount:
        return None
    account_link = kwargs.get("account_link")
    if account_link:
        if isinstance(account_link, DepartmentBudgetAccount) and account_link.department_id == dept_id:
            return account_link
        return None
    account_id = _normalize_finance_account(kwargs.get("account"))
    if not account_id:
        return None
    filters = {
        "department_id": dept_id,
        "account_id": account_id,
    }
    custom_account_name = kwargs.get("custom_account_name")
    if custom_account_name:
        filters["custom_account_name__iexact"] = custom_account_name
    return DepartmentBudgetAccount.objects.filter(**filters).first()


def _map_finance_right(right_code: str) -> Optional[str]:
    if not right_code:
        return None
    return FINANCE_RIGHT_FIELD_MAP.get(right_code.lower())


def _has_finance_right(dept_id: int, right_code: str, user, **kwargs) -> bool:
    role_field = _map_finance_right(right_code)
    if not role_field:
        return False
    link = _resolve_finance_link(dept_id, **kwargs)
    if not link:
        return False
    role_user = getattr(link, role_field, None)
    return role_user_id_safe(role_user) == role_user_id_safe(user)


def _has_finance_any_rights(dept_id: int, right_codes: Sequence[str], user, **kwargs) -> bool:
    normalized_codes = [field for field in (_map_finance_right(code) for code in right_codes) if field]
    if not normalized_codes:
        return False
    link = _resolve_finance_link(dept_id, **kwargs)
    if not link:
        return False
    user_id = role_user_id_safe(user)
    if not user_id:
        return False
    for field in normalized_codes:
        role_user = getattr(link, field, None)
        if role_user_id_safe(role_user) == user_id:
            return True
    return False


def role_user_id_safe(user_obj):
    return getattr(user_obj, "id", None)


# =============================
#    БИЗНЕС-ПРАВИЛА ДЛЯ ЗАЯВОК
# =============================

def dept_id_from_request(request_obj) -> Optional[int]:
    if request_obj is None:
        return None
    if hasattr(request_obj, "department_id"):
        return request_obj.department_id
    if hasattr(request_obj, "department") and request_obj.department:
        return request_obj.department.id
    return None

# Статусы (name-коды), сравниваем __iexact:
FINAL_STATES = {"done", "cancelled"}
APPROVED_STATES = {"approved", "in_progress", "done"}
EDITABLE_STATES = {"draft", "submitted"}  # автор/approver/po_manager могут редактировать (см. ниже)

def can_create_request(department_or_code, user: CustomUser) -> bool:
    # Requester или PO_manager в департаменте
    return has_any_dept_rights(department_or_code, ["Requester", "PO_manager"], user)

def can_view_request(request_obj, user: CustomUser) -> bool:
    dep_id = dept_id_from_request(request_obj)
    if dep_id is None:
        return False
    # Viewer/Approver/Requester/PO_manager видят заявки департамента
    if has_any_dept_rights(dep_id, ["Viewer", "Approver", "Requester", "PO_manager"],user):
        return True
    # Автор всегда видит свою заявку
    author = getattr(request_obj, "created_by", None) or getattr(request_obj, "author", None)
    return author == user

def can_edit_request(request_obj, user: CustomUser) -> bool:
    """
    Сейчас по твоим правилам: апрувер может менять количество/коммент,
    автор редактирует до финальных статусов, PO_manager по процессу.
    """
    dep_id = dept_id_from_request(request_obj)
    if dep_id is None:
        return False

    status = (getattr(request_obj, "status", None) or "").lower()
    is_final = status in FINAL_STATES

    author = getattr(request_obj, "created_by", None) or getattr(request_obj, "author", None)

    if author == user and not is_final:
        return True
    if has_dept_right(dep_id, "Approver",user) and not is_final:
        return True
    if has_dept_right(dep_id, "PO_manager", user) and not is_final:
        return True
    return False

def can_approve_request(request_obj, user: CustomUser) -> bool:
    dep_id = dept_id_from_request(request_obj)
    if dep_id is None:
        return False
    # Апрувер может утверждать, если не финальный статус
    status = (getattr(request_obj, "status", None) or "").lower()
    if status in FINAL_STATES:
        return False
    return has_dept_right( dep_id, "Approver", user)

def can_cancel_request(request_obj, user: CustomUser) -> bool:
    dep_id = dept_id_from_request(request_obj)
    if dep_id is None:
        return False
    status = (getattr(request_obj, "status", None) or "").lower()
    if status in FINAL_STATES:
        return False
    author = getattr(request_obj, "created_by", None) or getattr(request_obj, "author", None)
    if author == user:
        return True
    return has_dept_right(dep_id, "PO_manager", user)

def can_submit_po(request_obj, user: CustomUser) -> bool:
    dep_id = dept_id_from_request(request_obj)
    if dep_id is None:
        return False
    # PO можно после approve (и в in_progress, и далее — на твоё усмотрение)
    status = (getattr(request_obj, "status", None) or "").lower()
    if status not in APPROVED_STATES:
        return False
    return has_dept_right(dep_id, "PO_manager", user)

def can_notify_on_request_update(department_or_code, user: CustomUser) -> bool:
    # Любая из ролей-нотификаторов в департаменте
    for role in ("notifier", "notifier_rejected", "notifier_cancelled", "po_manager"):
        if has_notif_role(department_or_code, role, user):
            return True
    return False

# =============================
#     TEMPLATE TAGS (единый стиль: ..., user последним)
# =============================

@register.simple_tag
def has_right(department_or_code, user, right_code: str = "", module: str = "requests", **kwargs) -> bool:
    return has_dept_right(department_or_code, right_code, user, module=module, **kwargs)

@register.simple_tag
def has_any_rights(department_or_code, user, *right_codes, module: str = "requests", **kwargs) -> bool:
    return has_any_dept_rights(department_or_code, right_codes, user, module=module, **kwargs)

@register.simple_tag
def has_notif(department_or_code, user, role_code: str) -> bool:
    return has_notif_role(department_or_code, role_code, user)

@register.simple_tag
def can_create_request_tag(department_or_code, user) -> bool:
    return can_create_request(department_or_code, user)

@register.simple_tag
def can_view_request_tag(request_obj, user) -> bool:
    return can_view_request(request_obj, user)

@register.simple_tag
def can_edit_request_tag(request_obj, user) -> bool:
    return can_edit_request(request_obj, user)

@register.simple_tag
def can_approve_request_tag(request_obj, user) -> bool:
    return can_approve_request(request_obj, user)

@register.simple_tag
def can_cancel_request_tag(request_obj, user) -> bool:
    return can_cancel_request(request_obj, user)

@register.simple_tag
def can_submit_po_tag(request_obj, user) -> bool:
    return can_submit_po(request_obj, user)

@register.simple_tag
def can_notify_on_request_update_tag(department_or_code, user) -> bool:
    return can_notify_on_request_update(department_or_code, user)
