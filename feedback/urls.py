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
                                     login_url='account:log_in'), name='customers'),
    path(r'customer/edit/<customer_email>', login_required(views.customer_edit,
                                                           login_url='account:log_in'), name='customer_edit'),
    path(r'customer/survey/<customer_email>', login_required(views.customer_survey,
                                                             login_url='account:log_in'), name='customer_survey'),
    path(r'customer/notes/<customer_email>', login_required(views.customer_notes,
                                                            login_url='account:log_in'), name='customer_notes'),
    path(r'customer/add_note/<customer_email>', login_required(views.add_note,
                                                               login_url='account:log_in'), name='add_note'),
    path(r'customer/send_survey/<customer_email>', login_required(views.send_survey,
                                                                  login_url='account:log_in'), name='send_survey')
]
