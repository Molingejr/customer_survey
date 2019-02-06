from django.shortcuts import render


def home(request):
    """View for our home page"""
    return render(request, 'home.html')
