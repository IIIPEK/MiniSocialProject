from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

from .models import CustomUser, UserSetting

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'nickname','first_name', 'last_name',
            'avatar', 'date_of_birth', 'website',
            'telegram', 'whatsapp', 'viber',
            'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'telegram': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'viber': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        # можно сохранить дополнительные поля позже в профиль, если реализовать связь
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email',
            'avatar', 'bio', 'status_message',
            'location', 'website', 'date_of_birth',
            'telegram', 'whatsapp', 'viber',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status_message': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telegram': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'viber': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSetting
        fields = ['name', 'value']
        widgets = {
            'name': forms.HiddenInput(),  # имя параметра мы не даем менять
        }

# Если хотим редактировать несколько настроек за раз
class MultipleUserSettingsForm(forms.Form):
    chat_refresh_interval = forms.IntegerField(
        label="Интервал обновления чата (мс)",
        min_value=1000,
        max_value=60000,
        step_size=1000,
    )
    posts_per_page = forms.IntegerField(
        label="Количество постов на странице",
        min_value=5,
        max_value=100,
    )

    def save(self, user):
        from .models import UserSetting
        settings_map = {
            'CHAT_REFRESH_INTERVAL': self.cleaned_data['chat_refresh_interval'],
            'POSTS_PER_PAGE': self.cleaned_data['posts_per_page'],
        }
        for name, value in settings_map.items():
            UserSetting.objects.update_or_create(
                user=user, name=name, defaults={'value': str(value)}
            )
