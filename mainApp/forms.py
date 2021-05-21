from django import forms
from .models import Recipe

class recipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['cocktail_name', 'ingredients', 'image', 'category', 'duration', 'description', 'instruction']
        labels = {
            'image': 'Upload a photo of your drink',
            'instruction': 'Instructions'
        }