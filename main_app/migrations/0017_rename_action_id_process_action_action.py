# Generated by Django 3.2.4 on 2021-10-26 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_auto_20211026_1232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='process_action',
            old_name='action_id',
            new_name='action',
        ),
    ]