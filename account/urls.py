from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

"""Register our all url paths for our app"""

app_name = 'account'
urlpatterns = [
    path(r'signup', views.signup, name='signup'),
    path(r'login', views.log_in, name='log_in'),
    path(r'logout', views.user_logout, name='logout'),
    path(r'companies', login_required(views.CompanyListView.as_view(),
                                      login_url='account:log_in'), name='companies'),
    path(r'no-permission', views.no_permission, name='no_permission')
]
