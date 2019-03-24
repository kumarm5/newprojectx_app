from django.db import models
from projectx_app.models.user_detail import *

STATUS = (
    (True, 'Active'),
    (False, 'Inactive'),
)

# SYSTEM_VENDOR_TYPE = (
#     ('BGV', 'Back Ground Verification'),
#     ('RFC', 'Reference Check'),
#     ('HRF', 'HR Forms'),
# )


class Country(models.Model):
    country_name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Country Name')

    def __str__(self):
        return self.country_name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country')
    state_name = models.CharField(max_length=256, blank=True, null=True, verbose_name='State Name')

    def __str__(self):
        return self.state_name

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'


class TemplateType(models.Model):
    template_type_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.template_type_name

    class Meta:
        verbose_name = "Template Type"
        verbose_name_plural = "Template Types"


class CountryCode(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_code')
    country_code_name = models.CharField(max_length=256, verbose_name='Company Code')

    def __str__(self):
        return self.country_code_name

    class Meta:
        verbose_name = "Country Code"
        verbose_name_plural = "Country Codes"


class IDDocumentType(models.Model):
    document_name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Document Name')

    def __str__(self):
        return self.document_name

    class Meta:
        verbose_name = "ID Document Type"
        verbose_name_plural = "ID Document Types"


class DocumentType(models.Model):
    document_type_name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Document Type Name')

    def __str__(self):
        return self.document_type_name

    class Meta:
        verbose_name = "Document Type"
        verbose_name_plural = "Document Types"


class DocumentTypeName(models.Model):
    documenttype = models.ForeignKey(DocumentType, on_delete=models.CASCADE, related_name='document_type')
    document_name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Document Name')

    def __str__(self):
        return self.document_name

    class Meta:
        verbose_name = "Document Type Name"
        verbose_name_plural = "Document Type Names"


class SysVendorType(models.Model):
    type_description = models.CharField(max_length=30, verbose_name='Description')

    def __str__(self):
        return self.type_description

    class Meta:
        verbose_name = "System Vendor Type"
        verbose_name_plural = "System Vendor Types"


class SysRefCheck(models.Model):
    reference_name = models.CharField(max_length=50, verbose_name='Number of Reference')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.reference_name

    class Meta:
        verbose_name = 'System Reference Check'
        verbose_name_plural = 'System Reference Checks'
