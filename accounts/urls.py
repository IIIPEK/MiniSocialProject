from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('password/change/', views.password_change_view, name='password_change'),
    path('users/', views.user_list, name='user_list'),
    path('users/<str:username>/', views.public_profile, name='public_profile'),
    path('users/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
]
