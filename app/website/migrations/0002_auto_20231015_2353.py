# Generated by Django 4.2.6 on 2023-10-15 23:30

from django.db import migrations

def load_restaurant_data(apps, schem_editor):
    Restaurant = apps.get_model("website", "Restaurant")

    Restaurant(name="Hamburguesas", 
               description="Las mejores hamburguesas con los mejores chefs!").save()
    Restaurant(name="Tacos",
               description="Los mejores tacos del mundo!").save()

class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_restaurant_data)
    ]