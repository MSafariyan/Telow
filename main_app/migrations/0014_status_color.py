# Generated by Django 3.2.4 on 2021-10-26 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_auto_20211024_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='color',
            field=models.CharField(max_length=7, null=True),
        ),
    ]
