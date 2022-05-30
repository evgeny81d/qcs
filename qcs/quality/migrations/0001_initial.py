# Generated by Django 3.2 on 2022-05-30 04:56

from django.db import migrations, models
import django.db.models.deletion
import quality.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(help_text='Enter batch number', max_length=100, verbose_name='Batch number')),
                ('size', models.PositiveIntegerField(help_text='Enter batch size', verbose_name='Batch size')),
                ('m_date', models.DateField(help_text='Select manufacturing date', verbose_name='Manufacturing date')),
                ('exp_date', models.DateField(help_text='Select expiry date', verbose_name='Expiry date')),
                ('coa', models.FileField(blank=True, help_text='Select COA file to upload', upload_to=quality.models.coa_file_path, verbose_name='COA file')),
                ('product', models.ForeignKey(help_text='Select product', on_delete=django.db.models.deletion.PROTECT, related_name='batches', to='products.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': ('batch',),
                'verbose_name_plural': 'batches',
                'ordering': ['product', 'number'],
            },
        ),
    ]
