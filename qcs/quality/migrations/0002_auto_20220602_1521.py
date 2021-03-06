# Generated by Django 3.2 on 2022-06-02 12:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import quality.models


class Migration(migrations.Migration):

    dependencies = [
        ('quality', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batch',
            options={'ordering': ['product', 'number'], 'verbose_name': 'batch', 'verbose_name_plural': 'batches'},
        ),
        migrations.AlterField(
            model_name='batch',
            name='coa',
            field=models.FileField(blank=True, help_text='Select file to upload (pdf, jpg, jpeg, png, xls, xlsx, doc, docx)', null=True, upload_to=quality.models.coa_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png', 'xls', 'xlsx', 'doc', 'docx'], 'Invalid file extension'), quality.models.file_type_validator], verbose_name='Certificate of analysis'),
        ),
        migrations.CreateModel(
            name='ColorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='Record creation timestamp', verbose_name='Timestamp')),
                ('category', models.CharField(choices=[('CS', 'Color sheet'), ('QC', 'Quality check')], help_text='Select color data category', max_length=2, verbose_name='Category')),
                ('l_25', models.DecimalField(decimal_places=2, help_text='Enter L25 value', max_digits=5, verbose_name='L25')),
                ('l_45', models.DecimalField(decimal_places=2, help_text='Enter L45 value', max_digits=5, verbose_name='L45')),
                ('l_75', models.DecimalField(decimal_places=2, help_text='Enter L75 value', max_digits=5, verbose_name='L75')),
                ('a_25', models.DecimalField(decimal_places=2, help_text='Enter a25 value', max_digits=5, verbose_name='a25')),
                ('a_45', models.DecimalField(decimal_places=2, help_text='Enter a45 value', max_digits=5, verbose_name='a45')),
                ('a_75', models.DecimalField(decimal_places=2, help_text='Enter a75 value', max_digits=5, verbose_name='a75')),
                ('b_25', models.DecimalField(decimal_places=2, help_text='Enter b25 value', max_digits=5, verbose_name='b25')),
                ('b_45', models.DecimalField(decimal_places=2, help_text='Enter b45 value', max_digits=5, verbose_name='b45')),
                ('b_75', models.DecimalField(decimal_places=2, help_text='Enter b75 value', max_digits=5, verbose_name='b75')),
                ('de_25', models.DecimalField(decimal_places=2, help_text='Enter dE25 value', max_digits=5, verbose_name='dE25')),
                ('de_45', models.DecimalField(decimal_places=2, help_text='Enter dE45 value', max_digits=5, verbose_name='dE45')),
                ('de_75', models.DecimalField(decimal_places=2, help_text='Enter dE75 value', max_digits=5, verbose_name='dE75')),
                ('comment', models.TextField(blank=True, help_text='Enter comment', verbose_name='Comment')),
                ('batch', models.ForeignKey(help_text='Select batch', on_delete=django.db.models.deletion.PROTECT, related_name='color_data', to='quality.batch', verbose_name='Batch')),
            ],
        ),
    ]
