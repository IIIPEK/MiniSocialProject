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