from django.contrib import admin

from .models import AccountingAccount, DepartmentBudgetAccount


class DepartmentBudgetAccountInline(admin.TabularInline):
    model = DepartmentBudgetAccount
    extra = 1
    autocomplete_fields = (
        'department',
        'budget_approver',
        'budget_coordinator',
        'request_preparer',
    )


@admin.register(AccountingAccount)
class AccountingAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'common_name')
    search_fields = ('account_number', 'common_name')
    inlines = [DepartmentBudgetAccountInline]


@admin.register(DepartmentBudgetAccount)
class DepartmentBudgetAccountAdmin(admin.ModelAdmin):
    list_display = (
        'department',
        'account',
        'custom_account_name',
        'budget_approver',
        'budget_coordinator',
        'request_preparer',
    )
    search_fields = (
        'department__code',
        'department__description',
        'account__account_number',
        'account__common_name',
        'custom_account_name',
    )
    list_filter = ('department',)
    autocomplete_fields = (
        'department',
        'account',
        'budget_approver',
        'budget_coordinator',
        'request_preparer',
    )
