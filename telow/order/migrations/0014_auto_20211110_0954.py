# Generated by Django 3.2.8 on 2021-11-10 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_alter_order_meta_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_meta',
            name='id',
        ),
        migrations.AlterField(
            model_name='order_meta',
            name='order_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='order.order'),
        ),
    ]
