rights_sql = """
INSERT INTO accounts_right (id, name, description) VALUES (1, 'Approver', 'Утверждает приобретение по заявке');
INSERT INTO accounts_right (id, name, description) VALUES (2, 'Requester', 'Может создавать заявки');
INSERT INTO accounts_right (id, name, description) VALUES (3, 'Viewer', 'Может просматривать заявки');
INSERT INTO accounts_right (id, name, description) VALUES (4, 'PO_manager', 'Может создавать PO');
"""

notification_roles_sql = """
INSERT INTO accounts_notificationrole (id, name, description) VALUES (1, 'notifier', 'Отправка утвержденных заявок');
INSERT INTO accounts_notificationrole (id, name, description) VALUES (2, 'notifier_rejected', 'Рассылка при отклонении');
INSERT INTO accounts_notificationrole (id, name, description) VALUES (3, 'notifier_cancelled', 'Рассылка при отмене');
INSERT INTO accounts_notificationrole (id, name, description) VALUES (4, 'po_manager', 'PO manager');
"""

request_status = """
INSERT INTO requests_requeststatus (id, code, description) VALUES (1, 'draft', 'Черновик');
INSERT INTO requests_requeststatus (id, code, description) VALUES (2, 'submitted', 'Отправлена');
INSERT INTO requests_requeststatus (id, code, description) VALUES (3, 'approved', 'Утверждена');
INSERT INTO requests_requeststatus (id, code, description) VALUES (4, 'rejected', 'Отклонена');
INSERT INTO requests_requeststatus (id, code, description) VALUES (5, 'cancelled', 'Отменена');
INSERT INTO requests_requeststatus (id, code, description) VALUES (6, 'done', 'Выполнена');
INSERT INTO requests_requeststatus (id, code, description) VALUES (7, 'in_progress', 'Взята в работу');
"""