from django.db import models
from django.conf import settings
from projectx_app.models.user import User
from projectx_app.models.master import *
from projectx_app.models.user_detail import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from projectx_app.models.company import *


SERVICE_PROVIDER_TYPE = (
    ('external', 'External'),
    ('internal', 'Internal'),
)

STATUS = (
    (True, 'Active'),
    (False, 'Inactive'),
)


class VendorMaster(models.Model):
    vendor_company_name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Vendor Company Name')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='vendor_country')
    address = models.CharField(max_length=500, verbose_name='Address', null=True, blank=True)
    vendor_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Vendor Phone Number')
    vendor_admin = models.CharField(max_length=256, blank=True, null=True, verbose_name='Vendor Admin')
    service_provider_type = models.CharField(default='external', choices=SERVICE_PROVIDER_TYPE, max_length=256, blank=True, null=True)
    admin_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Vendor Admin Phone Number')
    country_code = models.ForeignKey(CountryCode, on_delete=models.CASCADE, related_name='vendor_country_code')
    area_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Vendor Phone Number')
    email = models.EmailField(max_length=256, blank=True, null=True, verbose_name='Email')
    tax_number = models.CharField(max_length=256, blank=True, null=True, verbose_name='Tax Number')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_master_owner', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.vendor_company_name

    class Meta:
        verbose_name = "Vendor Master"
        verbose_name_plural = "Vendor Masters"


class CompanyVendor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_user', blank=True, null=True)
    vendor = models.ForeignKey(VendorMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='vendor_master')
    company = models.ForeignKey(SystemCompanySetup, on_delete=models.CASCADE, null=True, blank=True, related_name='company_master')
    service_provider_type = models.CharField(default='external', choices=SERVICE_PROVIDER_TYPE, max_length=256, blank=True, null=True)
    status = models.BooleanField(choices=STATUS, max_length=20, blank=True, null=True)
    upload_contract = models.FileField(null=True, blank=True, verbose_name='Upload Contract')
    contract_start_date = models.CharField(max_length=30, null=True, blank=True, verbose_name='Contract Start Date')
    contract_end_date = models.CharField(max_length=30, null=True, blank=True, verbose_name='Contract End Date')
    sys_vendor_type = models.ForeignKey(SysVendorType, on_delete=models.CASCADE, null=True, blank=True, verbose_name='System Vendor Type')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_user_owner', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return self.user.first_name +' '+ self.user.last_name
        return self.vendor.vendor_company_name

    class Meta:
        verbose_name = "Company Vendor"
        verbose_name_plural = "Company Vendors"

    class Meta:
        unique_together = ("user", "company", "vendor")
