from django.db import models


class Supplier(models.Model):
    """Product supplier model."""

    name = models.CharField(
        verbose_name='Name',
        max_length=100,
        help_text='Enter supplier name'
    )
    country = models.CharField(
        verbose_name='Country',
        max_length=60,
        help_text='Enter supplier country'
    )

    city = models.CharField(
        verbose_name='City',
        max_length=60,
        help_text='Enter supplier city'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'supplier'
        verbose_name_plural = 'suppliers'

    def __str__(self):
        return f'{self.name} {self.country} {self.city}'


class Package(models.Model):
    """Package type model."""

    # Choices constants
    TOTE = 'TOTE'
    DRUM = 'DRUM'
    PALE = 'PALE'
    CANISTER = 'CANISTER'
    CAN = 'CAN'
    BAG = 'BAG'
    KG = 'KG'
    LTR = 'LTR'

    # Package type choices
    PKG_TYPE_CHOICES = [
        (TOTE, 'Tote'),
        (DRUM, 'Drum'),
        (PALE, 'Pale'),
        (CANISTER, 'Canister'),
        (CAN, 'Can'),
        (BAG, 'Bag')
    ]
    # UOM (Unit Of Measure) choices
    UOM_CHOICES = [
        (KG, 'kg'),
        (LTR, 'ltr')
    ]

    package_type = models.CharField(
        verbose_name='Package type',
        max_length=8,
        choices=PKG_TYPE_CHOICES,
        help_text='Select package type'
    )
    uom = models.CharField(
        verbose_name='Unit of measure',
        max_length=3,
        choices=UOM_CHOICES,
        help_text='Select unit of measure'
    )
    size = models.PositiveIntegerField(
        verbose_name='Package size',
        help_text='Enter package size'
    )

    class Meta:
        ordering = ['size']
        verbose_name = 'package'
        verbose_name_plural = 'packages'

    def __str__(self):
        return (f'{self.size} {self.get_uom_display()} '
                f'{self.get_package_type_display().lower()}')


class Product(models.Model):
    """Product model."""

    # Choices constants
    SB = 'SB'
    WB = 'WB'
    PD = 'PD'
    AC = 'AC'
    AM = 'AM'
    PT = 'PT'
    ED = 'ED'
    PR = 'PR'
    CB = 'CB'
    BC = 'BC'
    B1 = 'B1'
    B2 = 'B2'
    CC = 'CC'
    MC = 'MC'
    TH = 'TH'
    CS = 'CS'
    AD = 'AD'

    # Formula technology choices
    FORMULA_CHOICES = [
        (SB, 'Solventborne'),
        (WB, 'Waterborne'),
        (PD, 'Powder coating'),
        (AC, 'Acid'),
        (AM, 'Amine')
    ]
    # Layering system choices
    TYPE_CHOICES = [
        (PT, 'Pretreatment'),
        (ED, 'Electrocoat'),
        (PR, 'Primer'),
        (CB, 'Color base'),
        (BC, 'Base coat'),
        (B1, 'Base 1'),
        (B2, 'Base 2'),
        (CC, 'Clear coat'),
        (MC, 'Monocoat'),
        (TH, 'Thinner'),
        (CS, 'Cleaning solvent'),
        (AD, 'Additive')
    ]

    # Model fields
    product_id = models.CharField(
        verbose_name='Product id',
        max_length=50,
        help_text='Enter product id code',
        unique=True,
        blank=True,
        null=True
    )
    code = models.CharField(
        verbose_name='Product code',
        max_length=50,
        help_text='Enter product code'
    )
    name = models.CharField(
        verbose_name='Product name',
        max_length=100,
        help_text='Enter product name'
    )
    formula = models.CharField(
        verbose_name='Formula technology',
        max_length=2,
        choices=FORMULA_CHOICES,
        help_text='Select formula technology'
    )
    product_type = models.CharField(
        verbose_name='Product type',
        max_length=2,
        choices=TYPE_CHOICES,
        help_text='Select product type'
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        verbose_name='Supplier',
        help_text='Select supplier',
        related_name='products'
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Package',
        help_text='Select package type',
        related_name='products'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'{self.name}'
