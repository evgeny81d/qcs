import datetime

from django.test import TestCase
from django.conf import settings
from django.core.validators import FileExtensionValidator

from products.models import Product, Supplier, Package
from ..models import Batch, file_type_validator, coa_file_path, color_file_path


class BatchModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.package = Package.objects.create(
            package_type='TOTE',
            uom='KG',
            size=1000
        )
        cls.supplier = Supplier.objects.create(
            name='Company',
            country='Country',
            city='City'
        )
        cls.product = Product.objects.create(
            product_id='YZR123',
            code='234-2',
            name='some base coat 123',
            formula='WB',
            product_type='BC',
            supplier=cls.supplier,
            package=cls.package
        )
        cls.batch = Batch.objects.create(
            product=cls.product,
            number='bx123',
            size=3500,
            m_date=datetime.date(2022, 5, 31),
            exp_date=datetime.date(2022, 8, 31)
        )

    def test_model_field_names(self):
        """Test model field names."""
        # Prepare test data
        field_names = ['id', 'product', 'number', 'size', 'm_date', 'exp_date',
                       'coa']
        foreign_key_related_names = ['color_data']
        all_field_names = [*field_names, *foreign_key_related_names]
        # Run test
        self.assertEqual(
            len(Batch._meta.get_fields()),
            len(all_field_names),
            f'Incorrect number of fields in model {Batch}'
        )
        self.assertCountEqual(
            [field.name for field in Batch._meta.get_fields()],
            all_field_names,
            f'Incorrect model {Batch} field names'
        )

    def test_model_fields_verbose_name(self):
        """Test model fields verbose_name attributes."""
        # Prepare test data
        verbose_names = {
            'product': 'Product',
            'number': 'Batch number',
            'size': 'Batch size',
            'm_date': 'Manufacturing date',
            'exp_date': 'Expiry date',
            'coa': 'Certificate of analysis'
        }
        # Run test
        for field, value in verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Batch._meta.get_field(field).verbose_name,
                    value,
                    f'Incorrect <field: {field}.verbose_name> attribute'
                )

    def test_model_fields_help_text(self):
        """Test model fields help_text attributes."""
        # Prepare test data
        help_texts = {
            'product': 'Select product',
            'number': 'Enter batch number',
            'size': 'Enter batch size',
            'm_date': 'Select manufacturing date',
            'exp_date': 'Select expiry date',
            'coa': (f'Select file to upload '
                    f'({", ".join(settings.VALID_FILE_EXTENSIONS)})')
        }
        # Run test
        for field, value in help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Batch._meta.get_field(field).help_text,
                    value,
                    f'Incorrect <field: {field}.help_text> attribute'
                )

    def test_model_coa_field_validators(self):
        """Test model <field: coa.validators> attribute."""
        # Prepare test data
        validators = [FileExtensionValidator, file_type_validator]
        # Run test
        self.assertEqual(
            len(Batch._meta.get_field('coa').validators),
            len(validators),
            ('Incorrect number of validators in '
             '<field: coa.validators> attribute')
        )
        self.assertIsInstance(
            Batch._meta.get_field('coa').validators[0],
            validators[0],
            'Incorrect validator type in <field: coa.validators> attribute'
        )
        self.assertEqual(
            Batch._meta.get_field('coa').validators[1].__name__,
            validators[1].__name__,
            'Incorrect validator function in <field: coa.validators> attribute'
        )

    def test_model_fields_unique(self):
        """Test model fields unique attributes."""
        # Prepare test data
        unique_fields = ['id', ]
        # Run test
        for field in unique_fields:
            with self.subTest(field=field):
                self.assertTrue(
                    Batch._meta.get_field(field).unique,
                    f'Incorrect <field: {field}.unique> attribute'
                )

    def test_model_fields_null_is_true(self):
        """Test model fields null attribute."""
        # Prepare test data
        null_true_fields = ['coa', ]
        # Run test
        for field in null_true_fields:
            with self.subTest(field=field):
                self.assertTrue(
                    Batch._meta.get_field(field).null,
                    f'Incorrect <field: {field}.null> attribute'
                )

    def test_model_fields_blank_is_true(self):
        """Test model fields blank attribute."""
        # Prepare test data
        blank_true_fields = ['coa', ]
        # Run test
        for field in blank_true_fields:
            with self.subTest(field=field):
                self.assertTrue(
                    Batch._meta.get_field(field).blank,
                    f'Incorrect <field: {field}.blank> attribute'
                )

    def test_model_meta_class_attributes(self):
        """Test model class Meta attributes."""
        self.assertEqual(
            Batch._meta.ordering,
            ['product', 'number'],
            'Incorrect <class: Meta.ordering> attribute'
        )
        self.assertEqual(
            Batch._meta.verbose_name,
            'batch',
            'Incorrect <class: Meta.verbose_name> attribute'
        )
        self.assertEqual(
            Batch._meta.verbose_name_plural,
            'batches',
            'Incorrect <class: Meta.verbose_name_plural> attribute'
        )

    def test_model_object_name(self):
        """Test model's __str__() method."""
        self.assertEqual(
            str(BatchModelTest.batch),
            f'{BatchModelTest.batch.product} {BatchModelTest.batch.number}',
            ('Incorrect object name returned by __str__() method '
             f'in model {Batch}')
        )

    def test_coa_file_path_function(self):
        """Test coa_file_path() function (callable for upload_to argument)."""
        # Create test data
        dummy_batch = Batch(
            product=BatchModelTest.product,
            number='foo/bar',  # direcory creation threat by using '/'
            size=3500,
            m_date=datetime.date(2022, 5, 31),
            exp_date=datetime.date(2022, 8, 31)
        )
        # Run test
        self.assertEqual(
            coa_file_path(BatchModelTest.batch, 'test.jpg'),
            'coa/some base coat 123 bx123 coa.jpg',
            'Incorrect filepath for certificate of analysis'
        )
        self.assertEqual(
            coa_file_path(dummy_batch, 'test.jpg'),
            'coa/some base coat 123 foo bar coa.jpg',
            ("Incorrect filepath for certificate of analysis "
             "(directory creation threat with '/' in batch number)")
        )
