# messaging/forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            "rows": 2,
            "placeholder": "Введите сообщение...",
            "class": "form-control"
        })
    )

    class Meta:
        model = Message
        fields = ["content"]
