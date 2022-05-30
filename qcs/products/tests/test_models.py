from django.test import TestCase
from ..models import Product, Supplier, Package


class PackageModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.package = Package.objects.create(
            package_type='TOTE',
            uom='KG',
            size=1000
        )

    def test_model_field_names(self):
        """Test model field names."""
        # Prepare test data
        field_names = [
            'id', 'package_type', 'uom', 'size'
        ]
        foreign_key_related_names = [
            'products'
        ]
        all_field_names = [
            *field_names,
            *foreign_key_related_names
        ]
        # Run test
        self.assertEqual(
            len(Package._meta.get_fields()),
            len(all_field_names),
            f'Incorrect number of fields in model {Package}'
        )
        self.assertCountEqual(
            [field.name for field in Package._meta.get_fields()],
            all_field_names,
            f'Incorrect model {Package} field names'
        )

    def test_model_fields_verbose_name(self):
        """Test model fields verbose_name attributes."""
        # Prepare test data
        verbose_names = {
            'package_type': 'Package type',
            'uom': 'Unit of measure',
            'size': 'Package size'
        }
        # Run test
        for field, value in verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Package._meta.get_field(field).verbose_name,
                    value,
                    f'Incorrect <field: {field}.verbose_name> attribute'
                )

    def test_model_fields_help_text(self):
        """Test model fields help_text attributes."""
        # Prepare test data
        help_texts = {
            'package_type': 'Select package type',
            'uom': 'Select unit of measure',
            'size': 'Enter package size'
        }
        # Run test
        for field, value in help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Package._meta.get_field(field).help_text,
                    value,
                    f'Incorrect <field: {field}.help_text> attribute'
                )

    def test_model_fields_choises(self):
        """Test model fields choices attribute."""
        # Prepare test data
        field_choices_map = {
            'package_type': [('TOTE', 'Tote'), ('DRUM', 'Drum'),
                             ('PALE', 'Pale'), ('CANISTER',
                                                'Canister'), ('CAN', 'Can'),
                             ('BAG', 'Bag')],
            'uom': [('KG', 'kg'), ('LTR', 'ltr')]
        }
        for field, choices in field_choices_map.items():
            with self.subTest(field=field):
                self.assertCountEqual(
                    Package._meta.get_field(field).choices,
                    choices,
                    f'Incorrect <field: {field}.choices> attribute'
                )

    def test_model_meta_class_attributes(self):
        """Test model class Meta attributes."""
        self.assertEqual(
            Package._meta.ordering,
            ['size'],
            'Incorrect <class: Meta.ordering> attribute'
        )
        self.assertEqual(
            Package._meta.verbose_name,
            'package',
            'Incorrect <class: Meta.verbose_name> attribute'
        )
        self.assertEqual(
            Package._meta.verbose_name_plural,
            'packages',
            'Incorrect <class: Meta.verbose_name_plural> attribute'
        )

    def test_model_object_name(self):
        """Test model's __str__() method."""
        self.assertEqual(
            str(PackageModelTest.package),
            (f'{PackageModelTest.package.size} '
             f'{PackageModelTest.package.get_uom_display()} '
             f'{PackageModelTest.package.get_package_type_display().lower()}'),
            ('Incorrect object name returned by __str__() method '
             f'in model {Package}')
        )


class SupplierModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = Supplier.objects.create(
            name='Company',
            country='Country',
            city='City'
        )

    def test_model_field_names(self):
        """Test model field names."""
        # Prepare test data
        field_names = [
            'id', 'name', 'country', 'city'
        ]
        foreign_key_related_names = [
            'products'
        ]
        all_field_names = [
            *field_names,
            *foreign_key_related_names
        ]
        # Run test
        self.assertEqual(
            len(Supplier._meta.get_fields()),
            len(all_field_names),
            f'Incorrect number of fields in model {Supplier}'
        )
        self.assertCountEqual(
            [field.name for field in Supplier._meta.get_fields()],
            all_field_names,
            f'Incorrect model {Supplier} field names'
        )

    def test_model_fields_verbose_name(self):
        """Test model fields verbose_name attributes."""
        # Prepare test data
        verbose_names = {
            'name': 'Name',
            'country': 'Country',
            'city': 'City'
        }
        # Run test
        for field, value in verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Supplier._meta.get_field(field).verbose_name,
                    value,
                    f'Incorrect <field: {field}.verbose_name> attribute'
                )

    def test_model_fields_help_text(self):
        """Test model fields help_text attributes."""
        # Prepare test data
        help_texts = {
            'name': 'Enter supplier name',
            'country': 'Enter supplier country',
            'city': 'Enter supplier city'
        }
        # Run test
        for field, value in help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Supplier._meta.get_field(field).help_text,
                    value,
                    f'Incorrect <field: {field}.help_text> attribute'
                )

    def test_model_meta_class_attributes(self):
        """Test model class Meta attributes."""
        self.assertEqual(
            Supplier._meta.ordering,
            ['name'],
            'Incorrect <class: Meta.ordering> attribute'
        )
        self.assertEqual(
            Supplier._meta.verbose_name,
            'supplier',
            'Incorrect <class: Meta.verbose_name> attribute'
        )
        self.assertEqual(
            Supplier._meta.verbose_name_plural,
            'suppliers',
            'Incorrect <class: Meta.verbose_name_plural> attribute'
        )

    def test_model_object_name(self):
        """Test model's __str__() method."""
        self.assertEqual(
            str(SupplierModelTest.supplier),
            (f'{SupplierModelTest.supplier.name} '
             f'{SupplierModelTest.supplier.country} '
             f'{SupplierModelTest.supplier.city}'),
            ('Incorrect object name returned by __str__() method '
             f'in model {Supplier}')
        )


class ProductModelTest(TestCase):
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
            yzr='YZR123',
            code='234-2',
            name='Some-base coate 123',
            formula='WB',
            product_type='BC',
            supplier=cls.supplier,
            package=cls.package
        )

    def test_model_field_names(self):
        """Test model field names."""
        # Prepare test data
        field_names = ['id', 'yzr', 'code', 'name', 'formula', 'product_type',
                       'supplier', 'package']
        foreign_key_related_names = []
        all_field_names = [
            *field_names,
            *foreign_key_related_names
        ]
        # Run test
        self.assertEqual(
            len(Product._meta.get_fields()),
            len(all_field_names),
            f'Incorrect number of fields in model {Product}'
        )
        self.assertCountEqual(
            [field.name for field in Product._meta.get_fields()],
            all_field_names,
            f'Incorrect model {Product} field names'
        )

    def test_model_fields_verbose_name(self):
        """Test model fields verbose_name attributes."""
        # Prepare test data
        verbose_names = {
            'yzr': 'YZR code',
            'code': 'Product code',
            'name': 'Product name',
            'formula': 'Formula technology',
            'product_type': 'Product type',
            'supplier': 'Supplier',
            'package': 'Package'
        }
        # Run test
        for field, value in verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Product._meta.get_field(field).verbose_name,
                    value,
                    f'Incorrect <field: {field}.verbose_name> attribute'
                )

    def test_model_fields_help_text(self):
        """Test model fields help_text attributes."""
        # Prepare test data
        help_texts = {
            'yzr': 'Enter yzr code',
            'code': 'Enter product code',
            'name': 'Enter product name',
            'formula': 'Select formula technology',
            'product_type': 'Select product type',
            'supplier': 'Select supplier',
            'package': 'Select package type'
        }
        # Run test
        for field, value in help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Product._meta.get_field(field).help_text,
                    value,
                    f'Incorrect <field: {field}.help_text> attribute'
                )

    def test_model_fields_unique(self):
        """Test model fields unique attributes."""
        # Prepare test data
        unique_fields = ['id', 'yzr']
        # Run test
        for field in unique_fields:
            with self.subTest(field=field):
                self.assertTrue(
                    Product._meta.get_field(field).unique,
                    f'Incorrect <field: {field}.unique> attribute'
                )

    def test_model_fields_null_is_true(self):
        """Test model fields null attribute."""
        # Prepare test data
        null_true_fields = ['package', 'yzr']
        # Run test
        for field in null_true_fields:
            with self.subTest(field=field):
                self.assertTrue(
                    Product._meta.get_field(field).null,
                    f'Incorrect <field: {field}.null> attribute'
                )

    def test_model_fields_blank_is_true(self):
        """Test model fields blank attribute."""
        # Prepare test data
        blank_true_fields = ['package', 'yzr']
        # Run test
        for field in blank_true_fields:
            with self.subTest(field=field):
                self.assertTrue(
                    Product._meta.get_field(field).blank,
                    f'Incorrect <field: {field}.blank> attribute'
                )

    def test_model_fields_choises(self):
        """Test model fields choices attribute."""
        # Prepare test data
        field_choices_map = {
            'formula': [('SB', 'Solventborne'), ('WB', 'Waterborne'),
                        ('PD', 'Powder coating'), ('AC', 'Acid'), ('AM', 'Amine')],
            'product_type': [('PT', 'Pretreatment'), ('ED', 'Electrocoat'),
                             ('PR', 'Primer'), ('CB',
                                                'Color base'), ('BC', 'Base coat'),
                             ('B1', 'Base 1'), ('B2',
                                                'Base 2'), ('CC', 'Clear coat'),
                             ('MC', 'Monocoat'), ('TH', 'Thinner'),
                             ('CS', 'Cleaning solvent'), ('AD', 'Additive')]
        }
        for field, choices in field_choices_map.items():
            with self.subTest(field=field):
                self.assertCountEqual(
                    Product._meta.get_field(field).choices,
                    choices,
                    f'Incorrect <field: {field}.choices> attribute'
                )

    def test_model_meta_class_attributes(self):
        """Test model class Meta attributes."""
        self.assertEqual(
            Product._meta.ordering,
            ['name'],
            'Incorrect <class: Meta.ordering> attribute'
        )
        self.assertEqual(
            Product._meta.verbose_name,
            'product',
            'Incorrect <class: Meta.verbose_name> attribute'
        )
        self.assertEqual(
            Product._meta.verbose_name_plural,
            'products',
            'Incorrect <class: Meta.verbose_name_plural> attribute'
        )

    def test_model_object_name(self):
        """Test model's __str__() method."""
        self.assertEqual(
            str(ProductModelTest.product),
            ProductModelTest.product.name,
            ('Incorrect object name returned by __str__() method '
             f'in model {Product}')
        )
