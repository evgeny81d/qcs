import magic
from pathlib import PurePath

from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from products.models import Product


def coa_file_path(instance, filename):
    """Create Certificat Of Analysis filepath for upload."""
    # Add logger or handler if settings.COA_DIR directory does not exist
    return (f'{settings.COA_DIR}{instance.product}_'
            f'{instance.number}{PurePath(filename).suffix}')


def coa_file_type_validator(file_obj):
    """Certificate of analysis file type validator."""
    with file_obj.open() as f:
        file_type = magic.from_buffer(f.read(2048), mime=True)
        if file_type not in Batch.VALID_FILE_TYPES:
            raise ValidationError(
                "Invalid file type '%(file_type)s'",
                code='invalid_file_type',
                params={'file_type': file_type}
            )


class Batch(models.Model):
    """Batch model."""

    # Valid Certificate Of Analysis file extensions and file types
    VALID_FILE_EXTENSIONS = [
        'pdf', 'jpg', 'jpeg', 'gif', 'png', 'xls', 'xlsx', 'doc', 'docx'
    ]
    VALID_FILE_TYPES = [
        ('application/vnd.openxmlformats-officedocument'
         '.wordprocessingml.document'),
        'application/msword', 'image/jpeg', 'image/png', 'application/pdf',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ]

    # Model fields
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
                   f'({", ".join(VALID_FILE_EXTENSIONS)})'),
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                VALID_FILE_EXTENSIONS,
                'Invalid file extension'
            ),
            coa_file_type_validator
        ]
    )

    class Meta:
        ordering = ['product', 'number']
        verbose_name = 'batch'
        verbose_name_plural = 'batches'

    def __str__(self):
        return f'{self.product} {self.number}'
