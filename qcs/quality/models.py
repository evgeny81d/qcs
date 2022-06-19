import magic
from pathlib import PurePath

from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from products.models import Product


def coa_file_path(instance, filename):
    """Create Certificat Of Analysis filepath for upload."""
    # Prevent creation of directory when '/' appear in product name
    # or batch number
    product = str(instance.product).replace('/', ' ')
    number = str(instance.number).replace('/', ' ')
    # Add logger or handler if settings.COA_DIR directory does not exist
    return (f'{settings.COA_DIR}{product} {number} coa'
            f'{PurePath(filename).suffix}')


def color_file_path(instance, filename):
    """Create color sheet filepath for upload."""
    # Prevent creation of directory when '/' appear in product name
    # or batch number
    product = str(instance.product).replace('/', ' ')
    number = str(instance.number).replace('/', ' ')
    # Add logger or handler if settings.COA_DIR directory does not exist
    return (f'{settings.COLOR_DIR}{product} {number} '
            f'color{PurePath(filename).suffix}')


def file_type_validator(file_obj):
    """Certificate of analysis file type validator."""
    file_type = magic.from_buffer(file_obj.open().read(), mime=True)
    if file_type not in settings.VALID_FILE_TYPES:
        raise ValidationError(
            "Invalid file type '%(file_type)s'",
            code='invalid_file_type',
            params={'file_type': file_type}
        )


class Batch(models.Model):
    """Batch model."""

    product = models.ForeignKey(
        Product,
        verbose_name='Product',
        help_text='Select product',
        related_name='batches',
        on_delete=models.PROTECT
    )
    number = models.CharField(
        verbose_name='Batch number',
        help_text='Enter batch number',
        max_length=100
    )
    size = models.PositiveIntegerField(
        verbose_name='Batch size',
        help_text='Enter batch size'
    )
    m_date = models.DateField(
        verbose_name='Manufacturing date',
        help_text='Select manufacturing date'
    )
    exp_date = models.DateField(
        verbose_name='Expiry date',
        help_text='Select expiry date'
    )
    coa = models.FileField(
        upload_to=coa_file_path,
        verbose_name='Certificate of analysis',
        help_text=(f'Select file to upload '
                   f'({", ".join(settings.VALID_FILE_EXTENSIONS)})'),
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                settings.VALID_FILE_EXTENSIONS,
                'Invalid file extension'
            ),
            file_type_validator
        ]
    )

    color_sheet = models.FileField(
        upload_to=color_file_path,
        verbose_name='Color sheet',
        help_text=(f'Select file to upload '
                   f'({", ".join(settings.VALID_FILE_EXTENSIONS)})'),
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                settings.VALID_FILE_EXTENSIONS,
                'Invalid file extension'
            ),
            file_type_validator
        ]
    )

    class Meta:
        ordering = ['product', 'number']
        verbose_name = 'batch'
        verbose_name_plural = 'batches'

    def __str__(self):
        return f'{self.product} {self.number}'


class ColorData(models.Model):
    """Color data model."""

    # Choices constants
    CS = 'CS'
    QC = 'QC'

    # Category choices
    CATEGORY_CHOICES = [
        ('CS', 'Batch color sheet'),
        ('QC', 'Batch panel quality inspection')
    ]

    timestamp = models.DateTimeField(
        verbose_name='Timestamp',
        help_text='Record creation timestamp',
        auto_now_add=True
    )
    batch = models.ForeignKey(
        Batch,
        verbose_name='Batch',
        help_text='Select batch',
        related_name='color_data',
        on_delete=models.PROTECT
    )
    category = models.CharField(
        verbose_name='Category',
        help_text='Select color data category',
        max_length=2,
        choices=CATEGORY_CHOICES
    )
    l_25 = models.DecimalField(
        verbose_name='L25',
        help_text='Enter L25 value',
        max_digits=5,
        decimal_places=2
    )
    l_45 = models.DecimalField(
        verbose_name='L45',
        help_text='Enter L45 value',
        max_digits=5,
        decimal_places=2
    )
    l_75 = models.DecimalField(
        verbose_name='L75',
        help_text='Enter L75 value',
        max_digits=5,
        decimal_places=2
    )
    a_25 = models.DecimalField(
        verbose_name='a25',
        help_text='Enter a25 value',
        max_digits=5,
        decimal_places=2
    )
    a_45 = models.DecimalField(
        verbose_name='a45',
        help_text='Enter a45 value',
        max_digits=5,
        decimal_places=2
    )
    a_75 = models.DecimalField(
        verbose_name='a75',
        help_text='Enter a75 value',
        max_digits=5,
        decimal_places=2
    )
    b_25 = models.DecimalField(
        verbose_name='b25',
        help_text='Enter b25 value',
        max_digits=5,
        decimal_places=2
    )
    b_45 = models.DecimalField(
        verbose_name='b45',
        help_text='Enter b45 value',
        max_digits=5,
        decimal_places=2
    )
    b_75 = models.DecimalField(
        verbose_name='b75',
        help_text='Enter b75 value',
        max_digits=5,
        decimal_places=2
    )
    de_25 = models.DecimalField(
        verbose_name='dE25',
        help_text='Enter dE25 value',
        max_digits=5,
        decimal_places=2
    )
    de_45 = models.DecimalField(
        verbose_name='dE45',
        help_text='Enter dE45 value',
        max_digits=5,
        decimal_places=2
    )
    de_75 = models.DecimalField(
        verbose_name='dE75',
        help_text='Enter dE75 value',
        max_digits=5,
        decimal_places=2
    )
    comment = models.TextField(
        verbose_name='Comment',
        help_text='Enter comment',
        blank=True
    )

    class Meta:
        ordering = ['-timestamp', 'batch', 'category']
        verbose_name = 'color data'
        verbose_name_plural = 'color data'

    def __str__(self):
        return f'{self.batch} {str(self.get_category_display()).lower()}'
