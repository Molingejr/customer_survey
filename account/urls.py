from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

"""Register our all url paths for our app"""

app_name = 'account'
urlpatterns = [
    path(r'signup', views.signup, name='signup'),
    path(r'login', views.log_in, name='log_in'),
    path(r'logout', views.user_logout, name='logout'),
    path(r'password-reset/', auth_views.PasswordResetView.as_view(
        template_name="account/password_reset.html"
    ), name='password_reset'),
    path(r'password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="account/password_reset_done.html"
    ), name='password_reset_done'),
    path(r'password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html"
    ), name='password_reset_confirm'),
    path(r'password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_complete.html"
    ), name='password_reset_complete'),
]
