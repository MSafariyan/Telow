# Generated by Django 3.2.9 on 2021-12-11 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0029_alter_customer_operator'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='editable',
            field=models.BooleanField(default=True),
        ),
    ]
