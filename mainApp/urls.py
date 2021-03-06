from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('register', views.register),
    path('createaccount', views.createaccount),
    path('login', views.login),
    path('signedin', views.signedin),
    path('profile', views.userprofile),
    path('addcocktail', views.addcocktail),
    path('uploadrecipe', views.uploadrecipe),
    path('cocktailrecipe/<int:recipe_id>', views.cocktailprofile),
    path('deletecocktail/<int:recipe_id>', views.deletecocktail),
    path('editrecipe/<int:recipe_id>', views.editrecipe),
    path("favorite/<int:recipe_id>", views.favorite),
    path("unfavorite/<int:recipe_id>", views.unfavorite),
    path('logout', views.logout),
    path('generate_api_recipe', views.generate_api_recipe),
    path('search_drink', views.search_drink),
]

