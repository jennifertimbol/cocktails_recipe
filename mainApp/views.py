from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from .forms import recipeForm
import requests
import json

def homepage(request):
    # if 'curr_user' not in request.session:
    #     return redirect('/')
    # user = User.objects.get(id=request.session['curr_user'])
    response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php?f=a')
    all_cocktails = Recipe.objects.all()
    # print(response.json()['drinks'][0])
    # for key in response.json()['drinks']:
    #     print(key)

    context= {
        # 'user': user,
        'cocktails': response.json()['drinks'][:9],
        'all_cocktails': all_cocktails,
    }
    return render(request, 'homepage.html', context)

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
    response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php?f=a')
    cocktails = Recipe.objects.filter(posted_by=user)
    fav_cocktails = Recipe.objects.filter(favorited_by=user)
    favorite = Recipe.objects.all()
    #print(response.json()['drinks'][0])
    # for key in response.json()['drinks']:
    #     print(key)

    context= {
        'user': user,
        'cocktails': response.json()['drinks'][:6],
        'created_cocktails': cocktails,
        'favorite_cocktails': fav_cocktails,
        'favorites': favorite,
    }
    return render(request, "profilepage.html", context)

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
            return redirect(f'/cocktailrecipe/{form.id}')
    else:
        context = {
            'user':User.objects.get(id=request.session['curr_user']),
            'recipeForm':postedRecipeForm,
        }
        return render(request, "addcocktailform.html", context)
    return redirect('/profile')

def cocktailprofile(request, recipe_id):
    user = User.objects.get(id=request.session['curr_user'])
    cocktail = Recipe.objects.get(id=recipe_id)
    favorite = Recipe.objects.all()

    context= {
        'user': user,
        'cocktail': cocktail,
        'favorited_by': favorite,
    }
    return render(request, "cocktailrecipe.html", context)

def deletecocktail(request, recipe_id):
    if 'curr_user' not in request.session:
        return redirect('/')

    delete_recipe = Recipe.objects.get(id=recipe_id)
    delete_recipe.delete()
    return redirect('/profile')

def editrecipe(request, recipe_id):
    # if 'curr_user' not in request.session:
    #     return redirect('/')
    # user = User.objects.get(id=request.session['curr_id'])
    this_recipe = Recipe.objects.get(id=recipe_id)

    context = {
        # 'user': user,
        'cocktail': this_recipe,
        'recipeForm': recipeForm()
    }
    return render(request, 'edit_recipe.html', context)

def saveupdatedrecipe(request, recipe_id):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['curr_user'])
        curr_recipe = Recipe.objects.get(id=recipe_id)
        postedUpdatedRecipeForm = recipeForm(request.POST, instance=curr_recipe)
        if postedUpdatedRecipeForm.is_valid():
            form = postedUpdatedRecipeForm.save()
    else:
        context = {
            'user':user,
            'cocktail':curr_recipe,
            'recipeForm': recipeForm()
        }
        return render(request, 'editrecipe.html', context)
    return redirect(f'/cocktailrecipe/{curr_recipe.id}')
    
def favorite(request, recipe_id):
    user = User.objects.get(id=request.session['curr_user'])
    recipe = Recipe.objects.get(id=recipe_id)
    user.favorited_recipes.add(recipe)

    return redirect(f'/cocktailrecipe/{recipe_id}')

def unfavorite(request, recipe_id):
    user = User.objects.get(id=request.session['curr_user'])
    recipe = Recipe.objects.get(id=recipe_id)
    user.favorited_recipes.remove(recipe)

    return redirect(f'/cocktailrecipe/{recipe_id}')

def logout(request):
    request.session.flush()
    return redirect('/')

def generate_api_recipe(request):
    response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php?f=a')
    context = {
        'drink_name': response.Drink.json(),
        'drink_image': response.DrinkThumb.json(),
        'drink_instruction': response.Instructions.json()
    }
    return render(request, 'homepage.html', context)

