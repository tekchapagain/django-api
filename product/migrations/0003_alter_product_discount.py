# Generated by Django 5.1.1 on 2024-09-27 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]
