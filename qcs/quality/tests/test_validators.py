"""
Important notes on sample files directories

Sample file directories for coa_file_type_validator() tests:
'quality/test/invalid_sample_files' - danger sample files (html, scripts etc.)
'quality/test/valid_sample_files' - safe sample files (pdf, doc, png, etc.)

Keep in these directories files you'd like to use for test runs.
Be aware! File types are tested (not file extensions).
"""
import magic
from pathlib import Path
from dataclasses import dataclass

from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import file_type_validator


@dataclass
class DjangoFieldFileMimic():
    """Django FieldFile class imitation."""

    file_path: str

    def open(self):
        """Returns io.BufferReader."""
        self.file_obj = open(self.file_path, mode='rb')
        return self.file_obj


class CoaFileTypeValidatorTest(TestCase):

    def test_valid_file_types(self):
        """Test valid file types."""
        # Get directory with sample files 'quality/tests/valid_sample_files'
        valid_files_path = Path(__file__).parent / 'valid_sample_files'
        # Run test
        for file_path in valid_files_path.iterdir():
            django_field_file = DjangoFieldFileMimic(file_path)
            with self.subTest(django_field_file=django_field_file):
                self.assertIsNone(
                    file_type_validator(django_field_file)
                )
                self.assertFalse(
                    django_field_file.file_obj.closed,
                    'File object was closed by coa_file_type_validator()'
                )

    def test_invalid_file_types(self):
        """Test invalid file types."""
        # Prepare test data
        # Get directory with sample files 'quality/tests/invalid_sample_files'
        invalid_files_path = Path(__file__).parent / 'invalid_sample_files'
        error_message = 'Invalid file type {}'
        # Run test
        for file_path in invalid_files_path.iterdir():
            django_field_file = DjangoFieldFileMimic(file_path)
            with self.subTest(django_field_file=django_field_file):
                self.assertRaises(
                    ValidationError, file_type_validator, django_field_file
                )
                self.assertRaisesRegex(
                    ValidationError,
                    error_message.format(
                        repr(
                            magic.from_buffer(
                                django_field_file.open().read(),
                                mime=True
                            )
                        )
                    ),
                    file_type_validator,
                    django_field_file
                )
                self.assertFalse(
                    django_field_file.file_obj.closed,
                    'File object was closed by coa_file_type_validator()'
                )
