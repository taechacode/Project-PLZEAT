# Generated by Django 3.0.7 on 2020-06-09 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0010_auto_20200609_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='recipe_quantity',
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_level',
            field=models.CharField(choices=[('쉬움', '쉬움'), ('중급', '중급'), ('어려움', '어려움')], max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_time',
            field=models.IntegerField(null=True),
        ),
    ]
