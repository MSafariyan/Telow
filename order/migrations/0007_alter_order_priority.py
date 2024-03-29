# Generated by Django 3.2.4 on 2021-10-25 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_meta_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='priority',
            field=models.CharField(choices=[('DO OR DIE', 'Do or die'), ('Critical', 'Critical priority'), ('High', 'High priority'), ('Middle', 'Middle priority'), ('Low', 'Low priority')], default='Low', max_length=11),
        ),
    ]
