from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'homepage.html')

def homepage(request):
    return render(request, 'homepage.html')

    