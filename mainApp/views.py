from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from .forms import recipeForm

def homepage(request):
    context = {
        'curr_user': User.objects.get(id=request.session['curr_user'])
    }
    return render(request, 'homepage.html')

def register(request):
    return render(request, 'register.html')

def createaccount(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
                for key,value in errors.items():
                    messages.error(request, value)
                return redirect('/register')

        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw
        )
        request.session['curr_user'] = user.id
        return redirect('/profile')

def login(request):
    return render(request, 'login.html')

def signedin(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['email'])
        if user:
            log_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['curr_user'] = log_user.id
                return redirect('/profile')
        messages.error(request, "Email or password are incorrect.")
    return redirect('/login')

def userprofile(request):
    if 'curr_user' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['curr_user'])
    context= {
        'user': user
    }
    return render(request, "profilepage.html")

def addcocktail(request):
    context = {
        'user': User.objects.get(id=request.session['curr_user']),
        'recipeForm':recipeForm()
    }
    return render(request, "addcocktailform.html", context)

def uploadrecipe(request):
    if request.method == 'POST':
        posted_by = User.objects.get(id=request.session['curr_user'])
        postedRecipeForm = recipeForm(request.POST, request.FILES)
        if postedRecipeForm.is_valid():
            form = postedRecipeForm.save(commit=False)
            form.posted_by_id = posted_by.id
            form.save()
            return redirect('/profile')
    else:
        context = {
            'user':User.objects.get(id=request.session['curr_user']),
            'recipeForm':postedRecipeForm,
        }
        return render(request, "addcocktailform.html", context)
    return redirect('/profile')
def logout(request):
    request.session.flush()
    return redirect('/')

