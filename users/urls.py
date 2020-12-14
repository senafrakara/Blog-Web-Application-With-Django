from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import EditProfilePageView, UserAccountSettingsView, ShowProfilePageView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset_form.html',
             subject_template_name='users/password_reset_subject.txt',
             email_template_name='users/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('change_password/', views.change_password, name='change_password'),
    path('account_settings/',  UserAccountSettingsView.as_view(), name='user_account_settings'),
    path('user_profile/<int:pk>', ShowProfilePageView.as_view(), name='user_profile'),
    path('edit_profile_page/<int:pk>', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('favorite_list/', views.favorite_list, name='favorite_list')
]
