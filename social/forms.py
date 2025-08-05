from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Что у вас нового?'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['content']
#         widgets = {
#             'content': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 2,
#                 'placeholder': 'Оставьте комментарий...'
#             }),
#         }

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Напишите комментарий...',
            'class': 'form-control',
        })
    )

    class Meta:
        model = Comment
        fields = ['content']