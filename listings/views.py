from django.http import HttpResponse
from django.shortcuts import render
from .models import Property
from django.views import View

def home(request):
    return render(request, 'listings/home.html')

def property_list(request):
    pass

def property_detail(request, id):
    pass

def about(request):
    pass

def contact(request):
    pass