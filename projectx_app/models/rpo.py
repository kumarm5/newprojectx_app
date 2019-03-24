from django.db import models
from django.conf import settings
from projectx_app.models.user import User
from projectx_app.models.master import *


class SysRpo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sys_rpo_user', null=True, blank=True)
    rpo_id = models.CharField(max_length=15, null=True, blank=True, verbose_name='RPO ID')
    rpo_company_name = models.CharField(max_length=256, verbose_name='Company Name')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, related_name='rpo_country')
    address = models.TextField(null=True, blank=True, verbose_name='Address')
    phone_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone Number')
    company_admin = models.CharField(max_length=256, null=True, blank=True, verbose_name='Company Administrator')
    country_code = models.ForeignKey(CountryCode, on_delete=models.CASCADE, null=True, blank=True, related_name='country_code')
    area_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='Area Code')
    number =  models.CharField(max_length=30, null=True, blank=True, verbose_name='Number')
    email = models.EmailField(max_length=80, null=True, blank=True, verbose_name='Email')
    annual_contract_value = models.CharField(max_length=50, null=True, blank=True, verbose_name='Annual Contract Value')
    contract_start_date = models.CharField(max_length=30, null=True, blank=True, verbose_name='Contract Start Date')
    contract_end_date = models.CharField(max_length=30, null=True, blank=True, verbose_name='Contract End Date')
    upload_contract = models.FileField(max_length=100, null=True, blank=True, verbose_name='Upload Contract')
    tax_number = models.CharField(max_length=30, null=True, blank=True, verbose_name='Upload Contract')
    contract_status = models.BooleanField(choices=STATUS, max_length=256, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rpo_owner', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.rpo_company_name

    class Meta:
        verbose_name = "Recruitment Process Outsource"
        verbose_name_plural = "Recruitment Process Outsources"


class RPOUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rpo_user')
    rpo = models.ForeignKey(SysRpo, on_delete=models.CASCADE, related_name='sysrpo_user', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rpouser_owner', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "RPO User"
        verbose_name_plural = "RPO Users"
