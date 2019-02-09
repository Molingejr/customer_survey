from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView

from .forms import FeedBackFormA, FeedBackFormB, CustomerForm
from .models import Customer, Answer, Note
from .sms import send_survey_link


def home(request):
    """View for our home page"""
    return render(request, 'home.html')


def save_first_form(request):
    """
    View function to handle our create appointment form
    :param request: Contains our request object
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = FeedBackFormA(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # Get the customer who has the form's email and save relationship
            customer = Customer.objects.get(email=form.data['email'])
            answer = Answer()
            answer.customer_answer = form.data['experience']

            answer.customer = customer
            answer.save()

            # redirect to a new URL:
            if answer.customer_answer == "I am very satisfied and will refer my friends and family to you":
                return redirect("http://www.mdanswerx.com/happycustomer")
            elif answer.customer_answer == "I am not satisfied":
                return redirect(reverse("feedback:formB") + f"?email={form.data['email']}")

    # if a GET (or any other method) we'll create a blank form
    else:
        email = request.GET['email']
        customer = Customer.objects.get(email=email)
        form = FeedBackFormA(initial={'name': customer.name, 'email': customer.email, 'cellphone': customer.cellphone})

    return render(request, 'feedback_form.html', {'form': form})


def save_second_form(request):
    """
        View function to handle our create appointment form
        :param request: Contains our request object
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = FeedBackFormB(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # Retrieve email from query parameters
            email = request.GET['email']
            customer = Customer.objects.get(email=email)
            answer = Answer()

            answer.customer_answer = form.data['experience']

            answer.customer = customer
            answer.save()

            # redirect to a new URL:
            return redirect('feedback:home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FeedBackFormB()

    return render(request, 'feedback_form.html', {'form': form})


class CustomerListView(ListView):
    """Render customer list"""
    model = Customer


def create_survey(request):
    """
    This function sends renders a form and save user information on the database.
    It also calls our sms function to send a link to a user through sms
    :param request: Contains request Object
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CustomerForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # Try to see if customer already exist and save otherwise
            try:
                Customer.objects.get(email=form.data['email'])
            except Exception:
                form.save()

            # Get customer and send message to customer
            customer = Customer.objects.get(email=form.data['email'])
            send_survey_link(customer)
        # Redirect to our customer list
        return redirect(reverse('feedback:customers'))
    else:
        form = CustomerForm()

    return render(request, 'customer_form.html', {'form': form})
