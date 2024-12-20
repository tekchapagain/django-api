# Generated by Django 5.1.1 on 2024-10-02 03:40

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_product_detail_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='categories'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(null=True, verbose_name='Text'),
        ),
    ]
