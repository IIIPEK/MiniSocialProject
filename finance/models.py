from django.conf import settings
from django.db import models


class AccountingAccount(models.Model):
    """Справочник бухгалтерских счетов."""
    account_number = models.CharField("Бухгалтерский счёт", max_length=32, unique=True)
    common_name = models.CharField("Общее название", max_length=255)

    class Meta:
        ordering = ['account_number']
        verbose_name = "Бухгалтерский счёт"
        verbose_name_plural = "Бухгалтерские счёта"

    def __str__(self):
        return f"{self.account_number} — {self.common_name}"


class DepartmentBudgetAccount(models.Model):
    """
    Связь департамента и бух.счёта с ответственными пользователями.
    Реализует «многие-ко-многим» между Department и AccountingAccount.
    """
    department = models.ForeignKey(
        'accounts.Department',
        on_delete=models.CASCADE,
        related_name='budget_account_links',
    )
    account = models.ForeignKey(
        AccountingAccount,
        on_delete=models.CASCADE,
        related_name='department_links',
    )
    budget_approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budget_accounts_to_approve',
        help_text="Пользователь, который утверждает бюджет",
    )
    budget_coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budget_accounts_to_coordinate',
        help_text="Координатор бюджета (глава отдела)",
    )
    custom_account_name = models.CharField(
        "Уточняющее название бух.счёта",
        max_length=255,
        help_text="Название, которое вводится вручную для конкретной связки",
    )
    request_preparer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budget_accounts_to_prepare',
        help_text="Пользователь, который готовит заявку",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('department', 'account', 'custom_account_name')
        verbose_name = "Связка департамента и бух.счёта"
        verbose_name_plural = "Связки департаментов и бух.счетов"

    def __str__(self):
        return f"{self.department.code} -> {self.account.account_number} ({self.custom_account_name})"
