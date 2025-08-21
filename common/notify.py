# common/notify.py
from django.core.mail import send_mail
from django.conf import settings
from django.template.context_processors import request

from accounts.models import DepartmentNotificationRecipient, NotificationRole, CustomUser
from utils.notifications import create_notification

# def notify_status_change(request_obj):
#     current_status = request_obj.current_status()
#     subject = f"Статус заявки обновлён: {request_obj.title}"
#     body = f"Заявка «{request_obj.title}» теперь в статусе: {request_obj.current_status().status.description}."
#
#     recipients = set()
#
#     # уведомить заявителя
#     if request_obj.requester.email:
#         recipients.add(request_obj.requester.email)
#
#     # уведомить утверждающего
#     if request_obj.approver and request_obj.approver.email:
#         recipients.add(request_obj.approver.email)
#
#     # при rejected и cancelled уведомить всех с ролью "notifier_rejected" / "notifier_cancelled"
#     role_suffix = None
#     if current_status.status.code == 'approved':
#         role_suffix = 'notifier'
#     elif current_status.status.code == 'rejected':
#         role_suffix = 'notifier_rejected'
#     elif current_status.status.code == 'cancelled':
#         role_suffix = 'notifier_cancelled'
#
#     if role_suffix:
#         try:
#             role = NotificationRole.objects.get(name=role_suffix)
#             recipients.update(
#                 DepartmentNotificationRecipient.objects.filter(
#                     department=request_obj.department,
#                     role=role
#                 ).values_list('user__email', flat=True)
#             )
#         except NotificationRole.DoesNotExist:
#             pass
#
#
#     if recipients:
#         send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, list(recipients), fail_silently=False)

# маппинг статуса → (verb, роли)
STATUS_ROUTES = {
    'approved':  ('request_approved',  ['notifier', 'po_manager']),
    'rejected':  ('request_rejected',  ['notifier_rejected']),
    'cancelled': ('request_cancelled', ['notifier_cancelled']),
    'in_progress': ('po_created',     ['po_manager']),
    # дефолты:
    'submitted': ('request_status',   ['notifier']),
    'draft':     ('request_status',   ['notifier']),
    'done':      ('request_status',   ['notifier']),
}

def _role_id(code: str):
    try:
        return NotificationRole.objects.only('id').get(name__iexact=code).id
    except NotificationRole.DoesNotExist:
        return None

def _recipients_for_roles(department, role_codes):
    ids = set()
    for code in role_codes:
        rid = _role_id(code)
        if not rid:
            continue
        ids.update(
            DepartmentNotificationRecipient.objects
            .filter(department=department, role_id=rid)
            .values_list('user_id', flat=True)
        )
    return ids

def _build_request_url(req) -> str:
    # Строим абсолютную ссылку вида https://host/requests/<id>/
    base = getattr(settings, "SITE_URL", "").rstrip("/")
    return f"{base}{req.get_absolute_url()}" if base else req.get_absolute_url()


def notify_status_change(request_obj, actor: CustomUser | None = None, request=none):
    """
    Письмо + site-уведомления по изменению статуса заявки.
    actor — кто поменял статус (если не передан, попытаемся угадать).
    """
    current_status = request_obj.current_status()
    status_code = (current_status.status.code or '').lower()

    subject = f"Статус заявки обновлён: {request_obj.title}"
    body = f"""Заявка «{request_obj.title}» теперь в статусе: {current_status.status.description}.
    Перейти 
    """

    # ----- 1) EMAIL (как было у тебя)
    recipients_emails = set()
    if getattr(request_obj, 'requester', None) and request_obj.requester.email:
        recipients_emails.add(request_obj.requester.email)
    if getattr(request_obj, 'approver', None) and request_obj.approver and request_obj.approver.email:
        recipients_emails.add(request_obj.approver.email)

    verb, role_codes = STATUS_ROUTES.get(status_code, ('request_status', ['notifier']))
    if role_codes:
        role_recipients = DepartmentNotificationRecipient.objects.filter(
            department=request_obj.department,
            role__name__in=role_codes  # name сравнивается чувствительно; при желании __iexact
        ).values_list('user__email', flat=True)
        recipients_emails.update(role_recipients)

    if recipients_emails:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, list(recipients_emails), fail_silently=False)

    # ----- 2) SITE-уведомления (новое)
    # Собираем user_id тех же получателей (плюс заявителя)
    recipient_ids = set(_recipients_for_roles(request_obj.department, role_codes))
    if getattr(request_obj, 'requester_id', None):
        recipient_ids.add(request_obj.requester_id)
    if getattr(request_obj, 'approver_id', None):
        recipient_ids.add(request_obj.approver_id)

    # Не посылаем себе же
    if actor is None:
        actor = getattr(current_status, 'changed_by', None) or getattr(request_obj, 'approver', None) or getattr(request_obj, 'requester', None)
    if actor and actor.id in recipient_ids:
        recipient_ids.discard(actor.id)

    if recipient_ids:
        # Получаем объекты пользователей одним запросом
        for user in CustomUser.objects.filter(id__in=recipient_ids):
            # target=request_obj даёт кликабельную ссылку (см. get_absolute_url)
            create_notification(actor=actor or user, recipient=user, verb=verb, target=request_obj)