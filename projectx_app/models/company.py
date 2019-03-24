from django.db import models
from django.conf import settings
from projectx_app.models.user import User
from projectx_app.models.master import *
from projectx_app.models.user_detail import *
from projectx_app.models.rpo import *

RPO_PROVIDER_STATUS = (
    (True, 'Yes'),
    (False, 'No'),
)

class SystemCompanySetup(models.Model):
    company_id = models.CharField(max_length=15, null=True, blank=True, verbose_name='Company ID')
    company_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='Company Name')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='company_country', null=True, blank=True)
    address = models.TextField(null=True, blank=True, verbose_name='Address')
    finance_user_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='Finance User Name')
    finance_email = models.EmailField(max_length=256, null=True, blank=True, verbose_name='Finance Eamil')
    phone_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone Number')
    company_admin = models.CharField(max_length=256, null=True, blank=True, verbose_name='Company Administrator')
    country_code = models.ForeignKey(CountryCode, on_delete=models.CASCADE, null=True, blank=True, related_name='company_country_code')
    area_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='Area Code')
    number =  models.CharField(max_length=30, null=True, blank=True, verbose_name='Number')
    email = models.EmailField(max_length=80, null=True, blank=True, verbose_name='Email')
    annual_contract_value = models.CharField(max_length=50, null=True, blank=True, verbose_name='Annual Contract Value')
    contract_start_date = models.DateField(max_length=30, null=True, blank=True, verbose_name='Contract Start Date')
    contract_end_date = models.DateField(max_length=30, null=True, blank=True, verbose_name='Contract End Date')
    upload_contract = models.FileField(max_length=100, null=True, blank=True, verbose_name='Upload Contract')
    tax_number = models.CharField(max_length=30, null=True, blank=True, verbose_name='Upload Contract')
    contract_status = models.BooleanField(choices=STATUS, max_length=256, blank=True, null=True)
    rpo_provider = models.BooleanField(default=False, choices=RPO_PROVIDER_STATUS, blank=True, null=True, verbose_name='RPO Provider')
    logo_image = models.ImageField(blank=True, verbose_name='logo')
    rpo = models.ForeignKey(SysRpo, on_delete=models.CASCADE, related_name='company_rpo', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_owner', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.company_name) if self.company_name else ''

    class Meta:
        verbose_name = "System Company Setup"
        verbose_name_plural = "System Company Setups"


class CompanyUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_user')
    company = models.ForeignKey(SystemCompanySetup, on_delete=models.CASCADE, related_name='company_setup_user', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='companyuser_owner', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Company User"
        verbose_name_plural = "Company Users"


