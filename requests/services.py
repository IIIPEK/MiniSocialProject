# requests/services.py
from typing import Iterable
from accounts.models import Department, NotificationRole, DepartmentNotificationRecipient

def _role_id(code: str):
    return NotificationRole.objects.values_list("id", flat=True).filter(name__iexact=code).first()

def recipients_for_role(department_id: int, role_code: str) -> list[int]:
    rid = _role_id(role_code)
    if not rid:
        return []
    return list(
        DepartmentNotificationRecipient.objects
        .filter(department_id=department_id, role_id=rid)
        .values_list("user_id", flat=True)
    )

def emit_request_notification(event_code: str, req, actor) -> None:
    """
    event_code: 'approved' | 'rejected' | 'cancelled' | 'po_created' | ...
    Здесь только создаём уведомления в твоём notifications app (иконка с ссылкой на заявку).
    """
    dep_id = getattr(req, "department_id", None)
    if not dep_id:
        return

    # Примеры маршрутизации:
    routes = {
        "approved": ["notifier", "po_manager"],
        "rejected": ["notifier_rejected"],
        "cancelled": ["notifier_cancelled"],
        "po_created": ["po_manager"],
    }
    role_codes = routes.get(event_code, [])
    if not role_codes:
        return

    target_user_ids: set[int] = set()
    for code in role_codes:
        target_user_ids.update(recipients_for_role(dep_id, code))

    # Сюда — твоя логика создания Notification:
    # notifications.create_many(
    #   users=target_user_ids,
    #   title="Заявка {req.number} {event_code}",
    #   url=reverse('requests:detail', args=[req.id]),
    #   payload={...}
    # )
