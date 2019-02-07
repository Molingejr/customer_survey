from django.urls import path
from . import views

"""Register our all url paths for our app"""

app_name = 'feedback'
urlpatterns = [
    path('', views.home, name='home'),
    path('formA', views.save_first_form, name='formA'),
    path('formB', views.save_second_form, name='formB')
]
