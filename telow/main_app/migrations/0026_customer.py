# Generated by Django 3.2.8 on 2021-11-20 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0025_alter_process_action_process_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=55)),
                ('customer_family', models.CharField(max_length=55)),
                ('customer_mobile', models.CharField(max_length=11)),
                ('customer_phone', models.CharField(max_length=11)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
