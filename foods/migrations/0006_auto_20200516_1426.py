# Generated by Django 2.2.5 on 2020-05-16 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0005_auto_20200516_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
