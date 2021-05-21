# Generated by Django 3.2 on 2021-05-21 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_auto_20210521_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.CharField(choices=[('tequila', 'Tequila'), ('gin', 'Gin'), ('whiskey', 'Whiskey'), ('vodka', 'Vodka'), ('rum', 'Rum'), ('bourbon', 'Bourbon'), ('cognac', 'Cognac'), ('white wine', 'White Wine'), ('red wine', 'Red Wine'), ('champagne', 'Champagne'), ('beer', 'Beer')], default='tequila', max_length=15),
        ),
    ]
