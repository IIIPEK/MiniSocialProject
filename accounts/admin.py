# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, UserCorporateProfile, Department, Right,
    NotificationRole, UserDepartmentRight, DepartmentNotificationRecipient,
    UserSetting
)
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered


# ============ INLINE КЛАССЫ ============

class UserCorporateProfileInline(admin.StackedInline):
    """Inline для корпоративного профиля пользователя"""
    model = UserCorporateProfile
    can_delete = False
    extra = 0
    fields = ('employee_id', 'position', 'hire_date', 'is_active_employee')


class UserDepartmentRightInline(admin.TabularInline):
    """Inline для прав пользователя в департаментах"""
    model = UserDepartmentRight
    extra = 0
    autocomplete_fields = ['department', 'right']


class UserSettingInline(admin.TabularInline):
    """Inline для настроек пользователя"""
    model = UserSetting
    extra = 0


# ============ ОСНОВНОЙ АДМИН ПОЛЬЗОВАТЕЛЕЙ ============

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'username', 'email', 'nickname', 'first_name', 'last_name',
        'is_staff', 'is_email_confirmed', 'is_verified', 'has_corporate_access'
    )
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'is_verified',
        'is_email_confirmed', 'userdepartmentright__department'
    )

    fieldsets = (
                    (None, {'fields': ('username', 'nickname', 'password')}),
                ) + UserAdmin.fieldsets[1:] + (
                    ('Дополнительная информация', {
                        'fields': (
                            'avatar', 'bio', 'status_message', 'karma', 'is_verified',
                            'location', 'website', 'date_of_birth',
                            'telegram', 'whatsapp', 'viber',
                            'following', 'is_email_confirmed',
                        ),
                    }),
                )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': (
                'nickname', 'avatar', 'bio', 'status_message', 'karma', 'is_verified',
                'location', 'website', 'date_of_birth',
                'telegram', 'whatsapp', 'viber',
                'following', 'is_email_confirmed',
            ),
        }),
    )

    search_fields = ('username', 'email', 'first_name', 'last_name', 'nickname')
    ordering = ('username',)

    # Добавляем inlines
    inlines = [UserSettingInline]

    def get_inlines(self, request, obj):
        """Показывать корпоративные inlines только для корпоративных пользователей"""
        inlines = [UserSettingInline]

        if obj and obj.has_corporate_access:
            inlines.extend([UserCorporateProfileInline, UserDepartmentRightInline])
        elif obj:
            # Для обычных пользователей показываем возможность создать корп.профиль
            inlines.append(UserCorporateProfileInline)

        return inlines

    def has_corporate_access(self, obj):
        """Столбец для отображения наличия корпоративного доступа"""
        return obj.has_corporate_access

    has_corporate_access.boolean = True
    has_corporate_access.short_description = 'Корпоративный доступ'


# ============ АДМИНЫ ДЛЯ КОРПОРАТИВНЫХ МОДЕЛЕЙ ============

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')
    ordering = ('code',)


@admin.register(Right)
class RightAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(NotificationRole)
class NotificationRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(UserDepartmentRight)
class UserDepartmentRightAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'right')
    list_filter = ('department', 'right')
    search_fields = ('user__username', 'user__nickname', 'department__code', 'right__name')
    autocomplete_fields = ['user', 'department', 'right']


@admin.register(DepartmentNotificationRecipient)
class DepartmentNotificationRecipientAdmin(admin.ModelAdmin):
    list_display = ('department', 'role', 'user')
    list_filter = ('department', 'role')
    search_fields = ('user__username', 'user__nickname', 'department__code', 'role__name')
    autocomplete_fields = ['user', 'department', 'role']


@admin.register(UserCorporateProfile)
class UserCorporateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'position', 'hire_date', 'is_active_employee')
    list_filter = ('is_active_employee', 'hire_date')
    search_fields = ('user__username', 'user__nickname', 'employee_id', 'position')
    autocomplete_fields = ['user']


@admin.register(UserSetting)
class UserSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'value')
    list_filter = ('name',)
    search_fields = ('user__username', 'user__nickname', 'name')
    autocomplete_fields = ['user']
