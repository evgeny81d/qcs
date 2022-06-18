import datetime

from django.test import TestCase
from django.conf import settings
from django.core.validators import FileExtensionValidator

from products.models import Product, Supplier, Package
from ..models import (
    Batch, ColorData, file_type_validator, coa_file_path, color_file_path
)


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
        coa_field = Batch._meta.get_field('coa')
        # Run test
        self.assertEqual(
            len(coa_field.validators),
            len(validators),
            f'Incorrect number of validators in {coa_field}'
        )
        self.assertIsInstance(
            coa_field.validators[0],
            validators[0],
            f'Incorrect validator type in {coa_field}'
        )
        self.assertEqual(
            coa_field.validators[1].__name__,
            validators[1].__name__,
            f'Incorrect validator function in {coa_field}'
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
            number='foo/bar',  # cover direcory creation threat by using '/'
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


class ColorDataModelTest(TestCase):
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
        cls.color_data = ColorData.objects.create(
            batch=cls.batch,
            category='CS',
            l_25=100.00,
            l_45=100.00,
            l_75=100.00,
            a_25=50.00,
            a_45=50.00,
            a_75=50.00,
            b_25=50.00,
            b_45=50.00,
            b_75=50.00,
            de_25=5.00,
            de_45=5.00,
            de_75=5.00,
            comment='Comment'
        )

    def test_model_constants(self):
        """Test model constants values."""
        # Prepare test data
        choice_constants = {ColorData.CS: 'CS', ColorData.QC: 'QC'}
        # Run test
        for key, val in choice_constants.items():
            with self.subTest(key=key):
                self.assertEqual(key, val)
        self.assertEqual(
            len(choice_constants),
            len(ColorData.CATEGORY_CHOICES),
            (f'Model {ColorData} choice constants not equal to number '
             'of choice options')
        )

    def test_model_field_names(self):
        """Test model field names."""
        # Prepare test data
        field_names = ['id', 'timestamp', 'batch', 'category', 'l_25', 'l_45',
                       'l_75', 'a_25', 'a_45', 'a_75', 'b_25', 'b_45', 'b_75',
                       'de_25', 'de_45', 'de_75', 'comment', 'color_sheet']
        foreign_key_related_names = []
        all_field_names = [*field_names, *foreign_key_related_names]
        # Run test
        self.assertEqual(
            len(ColorData._meta.get_fields()),
            len(all_field_names),
            f'Incorrect number of fields in model {ColorData}'
        )
        self.assertCountEqual(
            [field.name for field in ColorData._meta.get_fields()],
            all_field_names,
            f'Incorrect model {ColorData} field names'
        )

    def test_model_fields_verbose_name(self):
        """Test model fields verbose_name attributes."""
        # Prepare test data
        verbose_names = {
            'timestamp': 'Timestamp',
            'batch': 'Batch',
            'category': 'Category',
            'l_25': 'L25',
            'l_45': 'L45',
            'l_75': 'L75',
            'a_25': 'a25',
            'a_45': 'a45',
            'a_75': 'a75',
            'b_25': 'b25',
            'b_45': 'b45',
            'b_75': 'b75',
            'de_25': 'dE25',
            'de_45': 'dE45',
            'de_75': 'dE75',
            'comment': 'Comment',
            'color_sheet': 'Color sheet'
        }
        # Run test
        for field, value in verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    ColorData._meta.get_field(field).verbose_name,
                    value,
                    f'Incorrect <field: {field}.verbose_name> attribute'
                )

    def test_model_fields_help_text(self):
        """Test model fields help_text attributes."""
        # Prepare test data
        help_texts = {
            'timestamp': 'Record creation timestamp',
            'batch': 'Select batch',
            'category': 'Select color data category',
            'l_25': 'Enter L25 value',
            'l_45': 'Enter L45 value',
            'l_75': 'Enter L75 value',
            'a_25': 'Enter a25 value',
            'a_45': 'Enter a45 value',
            'a_75': 'Enter a75 value',
            'b_25': 'Enter b25 value',
            'b_45': 'Enter b45 value',
            'b_75': 'Enter b75 value',
            'de_25': 'Enter dE25 value',
            'de_45': 'Enter dE45 value',
            'de_75': 'Enter dE75 value',
            'comment': 'Enter comment',
            'color_sheet': (f'Select file to upload '
                            f'({", ".join(settings.VALID_FILE_EXTENSIONS)})')
        }
        # Run test
        for field, value in help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    ColorData._meta.get_field(field).help_text,
                    value,
                    f'Incorrect <field: {field}.help_text> attribute'
                )

    def test_model_color_sheet_field_validators(self):
        """Test model <field: color_sheet.validators> attribute."""
        # Prepare test data
        validators = [FileExtensionValidator, file_type_validator]
        color_sheet_field = ColorData._meta.get_field('color_sheet')
        # Run test
        self.assertEqual(
            len(color_sheet_field.validators),
            len(validators),
            (f'Incorrect number of validators in model {color_sheet_field} '
             'field')
        )
        self.assertIsInstance(
            color_sheet_field.validators[0],
            validators[0],
            f'Incorrect validator type in {color_sheet_field} field'
        )
        self.assertEqual(
            color_sheet_field.validators[1].__name__,
            validators[1].__name__,
            f'Incorrect validator type in {color_sheet_field} field'
        )

    def test_model_fields_unique(self):
        """Test model fields unique attributes."""
        # Prepare test data
        unique_fields = ['id', ]
        # Run test
        for field in unique_fields:
            with self.subTest(field=field):
                self.assertTrue(
                    ColorData._meta.get_field(field).unique,
                    f'Incorrect <field: {field}.unique> attribute'
                )

    def test_model_fields_null_is_true(self):
        """Test model fields null attribute."""
        # Prepare test data
        null_true_fields = ['color_sheet', ]
        # Run test
        for field in null_true_fields:
            with self.subTest(field=field):
                self.assertTrue(
                    ColorData._meta.get_field(field).null,
                    f'Incorrect <field: {field}.null> attribute'
                )

    def test_model_fields_blank_is_true(self):
        """Test model fields blank attribute."""
        # Prepare test data
        blank_true_fields = ['comment', 'color_sheet']
        # Run test
        for field in blank_true_fields:
            with self.subTest(field=field):
                self.assertTrue(
                    ColorData._meta.get_field(field).blank,
                    f'Incorrect <field: {field}.blank> attribute'
                )

    def test_model_fields_auto_now_add_is_true(self):
        """Test model fields auto_now_add attribute."""
        # Prepare test data
        blank_true_fields = ['timestamp', ]
        # Run test
        for field in blank_true_fields:
            with self.subTest(field=field):
                self.assertTrue(
                    ColorData._meta.get_field(field).auto_now_add,
                    f'Incorrect <field: {field}.blank> attribute'
                )

    def test_model_fields_max_digits_attribute(self):
        """Test model fields max_digits attribute."""
        # Prepare test data
        fields = ['l_25', 'l_45', 'l_75', 'a_25', 'a_45', 'a_75',
                  'b_25', 'b_45', 'b_75', 'de_25', 'de_45', 'de_75']
        # Run test
        for field in fields:
            with self.subTest(field=field):
                self.assertEqual(
                    ColorData._meta.get_field(field).max_digits,
                    5,
                    f'Incorrect <field: {field}.max_digits> attribute'
                )

    def test_model_fields_decimal_places_attribute(self):
        """Test model fields decimal places attribute."""
        # Prepare test data
        fields = ['l_25', 'l_45', 'l_75', 'a_25', 'a_45', 'a_75',
                  'b_25', 'b_45', 'b_75', 'de_25', 'de_45', 'de_75']
        # Run test
        for field in fields:
            with self.subTest(field=field):
                self.assertEqual(
                    ColorData._meta.get_field(field).max_digits,
                    5,
                    f'Incorrect <field: {field}.max_digits> attribute'
                )

    def test_model_meta_class_attributes(self):
        """Test model class Meta attributes."""
        self.assertEqual(
            ColorData._meta.ordering,
            ['-timestamp', 'batch', 'category'],
            'Incorrect <class: Meta.ordering> attribute'
        )
        self.assertEqual(
            ColorData._meta.verbose_name,
            'color data',
            'Incorrect <class: Meta.verbose_name> attribute'
        )
        self.assertEqual(
            ColorData._meta.verbose_name_plural,
            'color data',
            'Incorrect <class: Meta.verbose_name_plural> attribute'
        )

    def test_model_object_name(self):
        """Test model's __str__() method."""
        # Prepare test data
        color_data_obj = ColorDataModelTest.color_data
        batch_obj = ColorDataModelTest.batch
        self.assertEqual(
            str(color_data_obj),
            (f'{batch_obj} '
             f'{color_data_obj.get_category_display()}'.lower()),
            ('Incorrect object name returned by __str__() method '
             f'in model {ColorData}')
        )

    def test_color_file_path_function(self):
        """Test coa_file_path() function (callable for upload_to argument)."""
        # Create test data
        dummy_batch = Batch(
            product=BatchModelTest.product,
            number='foo/bar',  # cover direcory creation threat by using '/'
            size=3500,
            m_date=datetime.date(2022, 5, 31),
            exp_date=datetime.date(2022, 8, 31)
        )
        dummy_color = ColorData(
            batch=dummy_batch,
        )
        # Run test
        self.assertEqual(
            color_file_path(ColorDataModelTest.color_data, 'test.jpg'),
            'color/some base coat 123 bx123 color.jpg',
            'Incorrect filepath for certificate of analysis'
        )
        self.assertEqual(
            color_file_path(dummy_color, 'test.jpg'),
            'color/some base coat 123 foo bar color.jpg',
            ("Incorrect filepath for certificate of analysis "
             "(directory creation threat with '/' in batch number)")
        )
