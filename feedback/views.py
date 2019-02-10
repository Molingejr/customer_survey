from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import ListView

from .forms import FeedBackFormA, FeedBackFormB, CustomerForm, NoteForm
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
            answer.comment = ""

            answer.customer = customer
            # Try to get the latest survey id
            try:
                latest_id = Answer.objects.latest('survey_id')
                answer.survey_id = latest_id.survey_id + 1
            except Exception as exp:
                answer.survey_id = 1

            answer.save()

            # redirect to a new URL:
            if answer.customer_answer == "I am very satisfied and will refer my friends and family to you":
                return redirect("http://www.mdanswerx.com/happycustomer")
            elif answer.customer_answer == "I am not satisfied":
                return redirect(reverse("feedback:formB") + f"?email={form.data['email']}&survey_id={answer.survey_id}")

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
            survey_id = request.GET['survey_id']
            customer = Customer.objects.get(email=email)
            answer = Answer()

            answer.customer_answer = form.data['experience']
            answer.comment = form.data['comment']

            answer.customer = customer
            answer.survey_id = survey_id
            answer.save()

            # try:
            #     from .mail import send_email
            #     send_email(customer, answer.survey_id)
            # except Exception as exp:
            #     print(exp)

            # redirect to a new URL:
            return HttpResponse("<h2>Thank you for participating</h2>")

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
        return redirect('feedback:customers')
    else:
        form = CustomerForm()

    return render(request, 'customer_form.html', {'form': form})


def customer_edit(request, customer_email=None):
    """
        This function sends renders a form and updates customer information on the database.
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
            customer.name = form.data['name']
            customer.email = form.data['email']
            customer.cellphone = form.data['cellphone']
            customer.save()

        # Redirect to our customer list
        return redirect('feedback:customers')
    else:
        customer = Customer.objects.get(email=customer_email)
        form = CustomerForm(initial={"name": customer.name, "email": customer.email,
                                     "cellphone": customer.cellphone})

    return render(request, 'customer_edit_form.html', {'form': form})


def customer_survey(request, customer_email=None):
    """
    Get survey results for a customer
    :param request: Request object
    :param customer_email: customer's email
    :return: render customer survey page
    """
    customer = Customer.objects.get(email=customer_email)
    answers = Answer.objects.filter(customer=customer).order_by('survey_id')

    print(answers)
    return render(request, 'customer_survey_details.html', {'answers': answers, 'customer': customer})


def customer_notes(request, customer_email=None):
    """
    Get all notes for a customer
    :param request: Request object
    :param customer_email: customer's email
    :return: render customer notes page
    """
    customer = Customer.objects.get(email=customer_email)
    notes = Note.objects.filter(customer=customer)
    return render(request, 'customer_note_list.html', {'notes': notes, 'customer': customer})


def add_note(request, customer_email=None):
    """
    Get all notes for a customer
    :param request: Request object
    :param customer_email: customer's email
    :return: render page to add notes to customer profile
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NoteForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # Get customer and send message to customer
            customer = Customer.objects.get(email=customer_email)
            note = Note(title=form.data['title'], content=form.data['content'])
            note.customer = customer
            note.save()

        # Redirect to our customer list
        return redirect(reverse('feedback:customer_notes', args=[customer_email]))
    else:
        form = NoteForm()

    return render(request, 'customer_note_form.html', {'form': form})


def send_survey(request, customer_email):
    """
    Get all notes for a customer
    :param request: Request object
    :param customer_email: customer's email
    :return: render page to add notes to customer profile
    """
    customer = Customer.objects.get(email=customer_email)
    send_survey_link(customer)
    return redirect(reverse('feedback:customer_survey', args=[customer_email]))
