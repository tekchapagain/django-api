# Generated by Django 5.1.1 on 2024-09-29 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_product_review_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='review_count',
            new_name='reviews_count',
        ),
    ]
