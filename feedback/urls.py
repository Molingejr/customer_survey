from django.urls import path
from . import views

"""Register our all url paths for our app"""

app_name = 'feedback'
urlpatterns = [
    path('', views.home, name='home'),
]
