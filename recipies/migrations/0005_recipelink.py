# Generated by Django 3.0.7 on 2020-06-09 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0004_auto_20200609_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='recipies.Recipe')),
            ],
        ),
    ]
