# Generated by Django 5.0.3 on 2024-06-08 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_ordermodel_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='order_quantity',
            field=models.IntegerField(),
        ),
    ]
