from django.db import models
import re
import bcrypt
from PIL import Image

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors["first_name"] = "Name should be atleast 2 characters long" 
        if len(postData['last_name'])  < 1:
            errors["last_name"] = "You must enter a last name"   
        if len(postData['email']) == 0:
            errors["email"] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors["email"] = "Your email must be valid"
        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0 :
            errors["duplicate"] = "Email input is already in use"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['pw_match'] = "Password must match!"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=55)
    password = models.CharField(max_length=45)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

CATEGORY_CHOICES = (
    ('tequila', 'Tequila'),
    ('gin', 'Gin'),
    ('whiskey', 'Whiskey'),
    ('vodka', 'Vodka'),
    ('rum', 'Rum'),
    ('bourbon', 'Bourbon'),
    ('cognac', 'Cognac'),
    ('white wine', 'White Wine'),
    ('red wine', 'Red Wine'),
    ('champagne', 'Champagne'),
    ('beer', 'Beer'),
)

class Recipe(models.Model):
    cocktail_name = models.CharField(max_length=70)
    ingredients = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='media/')
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.weight > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default="tequila")
    duration = models.IntegerField()
    description = models.TextField()
    instruction = models.TextField()
    favorited_by = models.ManyToManyField(User, related_name="favorited_recipes")
    posted_by = models.ForeignKey(User, related_name="drinks", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

# class Comment(models.Model):
#     message = models.TextField()
#     commented_by = models.ForeignKey(User, related_name="poster", on_delete=models.CASCADE)
#     recipe_comments = models.ManyToManyField(Recipe, related_name="recipes")
#     created_at = models.DateField(auto_now_add=True)

