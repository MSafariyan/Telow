# Generated by Django 3.2.4 on 2021-10-27 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0021_auto_20211027_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='process_name',
            field=models.CharField(max_length=155, unique=True),
        ),
    ]
