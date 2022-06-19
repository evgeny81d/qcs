# Generated by Django 3.2 on 2022-06-19 10:39

import django.core.validators
from django.db import migrations, models
import quality.models


class Migration(migrations.Migration):

    dependencies = [
        ('quality', '0003_auto_20220602_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colordata',
            name='color_sheet',
        ),
        migrations.AddField(
            model_name='batch',
            name='color_sheet',
            field=models.FileField(blank=True, help_text='Select file to upload (pdf, jpg, jpeg, png, xls, xlsx, doc, docx)', null=True, upload_to=quality.models.color_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png', 'xls', 'xlsx', 'doc', 'docx'], 'Invalid file extension'), quality.models.file_type_validator], verbose_name='Color sheet'),
        ),
        migrations.AlterField(
            model_name='colordata',
            name='category',
            field=models.CharField(choices=[('CS', 'Batch color sheet'), ('QC', 'Batch panel quality inspection')], help_text='Select color data category', max_length=2, verbose_name='Category'),
        ),
    ]