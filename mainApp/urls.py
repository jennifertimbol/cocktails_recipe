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
    path('logout', views.logout),
    
]
