from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

"""Register our all url paths for our app"""

app_name = 'feedback'
urlpatterns = [
    path('', views.home, name='home'),
    path(r'formA', views.save_first_form, name='formA'),
    path('formB', views.save_second_form, name='formB'),
    path('create_survey', login_required(views.create_survey,
                                         login_url='account:log_in'), name='create_survey'),
    path('customers', login_required(views.CustomerListView.as_view(),
                                     login_url='account:log_in'), name='customers')
]
