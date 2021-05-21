from django.shortcuts import render, redirect, HttpResponse

def index(request):
    return render(request, "home.html")

# Create your views here.