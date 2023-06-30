# Generated by Django 4.2.2 on 2023-06-29 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='total',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
