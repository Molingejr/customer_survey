from django.urls import path
from . import views

"""Register our all url paths for our app"""

app_name = 'account'
urlpatterns = [
    path(r'signup', views.signup, name='signup'),
    path(r'login', views.log_in, name='log_in'),
    path(r'logout', views.user_logout, name='logout'),
]
