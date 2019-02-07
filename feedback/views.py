from django.shortcuts import render, redirect
from .forms import FeedBackFormA, FeedBackFormB
from .models import Customer, Answer, Note


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
            # process the data in form.cleaned_data as required
            customer = Customer()
            answer = Answer()
            answer.customer_answer = form.data['experience']

            # Todo: Save foreign key relationship of answer and customer
            # answer.customer = customer
            # answer.save()

            # redirect to a new URL:
            if answer.customer_answer == "I am very satisfied and will refer my friends and family to you":
                return redirect("http://www.mdanswerx.com/happycustomer")
            elif answer.customer_answer == "I am not satisfied":
                return redirect('feedback:formB')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FeedBackFormA()

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
            # process the data in form.cleaned_data as required
            customer = Customer()
            answer = Answer()

            answer.customer_answer = form.fields['experience']

            # Todo: Save foreign key relationship of answer and customer
            # answer.customer = customer
            # answer.save()

            # redirect to a new URL:
            return redirect('feedback:home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FeedBackFormB()

    return render(request, 'feedback_form.html', {'form': form})
