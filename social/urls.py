#social/urls.py
from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('posts/', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/like/', views.post_like_toggle, name='post_like_toggle'),
    # path('posts/<int:post_id>/comment/', views.comment_add, name='comment_add'),
    path('comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    # path('notifications/', views.notification_list, name='notification_list'),
]
