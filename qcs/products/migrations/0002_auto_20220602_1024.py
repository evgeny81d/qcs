# Generated by Django 3.2 on 2022-06-02 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='yzr',
        ),
        migrations.AddField(
            model_name='product',
            name='product_id',
            field=models.CharField(blank=True, help_text='Enter product_id code', max_length=50, null=True, unique=True, verbose_name='Product id'),
        ),
    ]
