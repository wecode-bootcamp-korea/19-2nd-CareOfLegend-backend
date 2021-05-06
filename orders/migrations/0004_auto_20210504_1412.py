# Generated by Django 3.2 on 2021-05-04 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_shipment_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipment_cost',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]