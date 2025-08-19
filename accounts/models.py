# accounts/models.py
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Now

def user_avatar_path(instance, filename):
    return f'avatars/user_{instance.id}/{filename}'


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True, db_default='')
    bio = models.TextField(blank=True, db_default="")
    status_message = models.CharField(max_length=100, blank=True, help_text='Девиз или настроение', db_default="")
    karma = models.IntegerField(db_default=0)
    is_verified = models.BooleanField(db_default=False)
    location = models.CharField(max_length=100, blank=True,db_default="")
    website = models.URLField(blank=True,db_default="")
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_default=Now())
    telegram = models.CharField(max_length=50, blank=True, db_default="")
    whatsapp = models.CharField(max_length=50, blank=True, db_default="")
    viber = models.CharField(max_length=50, blank=True, db_default="")
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    is_email_confirmed = models.BooleanField(default=False)
    nickname = models.CharField(max_length=50, unique=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.nickname

    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    @property
    def is_fully_active(self):
        """
        Гибкая проверка, разрешена ли активность:
        - подтверждён email
        - не заблокирован (в будущем можно добавить поле is_banned)
        """
        return self.is_active and self.is_email_confirmed

    @property
    def has_corporate_access(self):
        """Проверяет, есть ли у пользователя корпоративный доступ"""
        return hasattr(self, 'corporate_profile')

    def has_department_right(self, department_code, right_name):
        """
        Проверка права пользователя в департаменте
        """
        if not self.has_corporate_access:
            return False

        return UserDepartmentRight.objects.filter(
            user=self,
            department__code=department_code,
            right__name=right_name
        ).exists()

    def get_departments(self):
        """
        Получить все департаменты пользователя
        """
        if not self.has_corporate_access:
            return Department.objects.none()

        return Department.objects.filter(
            userdepartmentright__user=self
        ).distinct()


class UserSetting(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="settings"
    )
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.user.nickname} - {self.name} = {self.value}"


# ============ КОРПОРАТИВНАЯ СИСТЕМА (из Request_Project) ============

class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} — {self.description}"


class Right(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class NotificationRole(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class UserCorporateProfile(models.Model):
    """
    Корпоративная информация пользователя - опциональное расширение
    Создается только для пользователей, которым нужен доступ к системе заявок
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='corporate_profile'
    )
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True)
    hire_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active_employee = models.BooleanField(default=True)

    def __str__(self):
        return f"Corporate: {self.user.nickname} ({self.employee_id})"


class UserDepartmentRight(models.Model):
    """Права пользователя в департаментах"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    right = models.ForeignKey(Right, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'department', 'right')

    def __str__(self):
        return f"{self.user.nickname} / {self.department.code} / {self.right.name}"


class DepartmentNotificationRecipient(models.Model):
    """Получатели уведомлений по ролям в департаментах"""
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey(NotificationRole, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('department', 'role', 'user')

    def __str__(self):
        return f"{self.department.code} - {self.role.name} - {self.user.nickname}"

