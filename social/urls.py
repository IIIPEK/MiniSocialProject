from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/like/', views.post_like_toggle, name='post_like_toggle'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
