# Generated by Django 3.2.8 on 2021-11-10 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_auto_20211101_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_meta',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order', unique=True),
        ),
    ]