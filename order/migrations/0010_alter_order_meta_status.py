# Generated by Django 3.2.4 on 2021-10-28 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_alter_process_process_name'),
        ('order', '0009_auto_20211027_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_meta',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.status'),
        ),
    ]