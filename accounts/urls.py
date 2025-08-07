from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
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
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset_form.html',
             email_template_name='accounts/password_reset_email.html',
             success_url=reverse_lazy('accounts:password_reset_done')  # ✅ явно указано с namespace
         ),
         name='password_reset'
         ),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html',
                                                  ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',
                                                     success_url=reverse_lazy('accounts:password_reset_complete'), ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('resend_activation/', views.resend_activation_email, name='resend_activation'),

]
