from django.db import models
from django.conf import settings
from projectx_app.models.user import User
from projectx_app.models.master import *
from projectx_app.models.request import *
from projectx_app.models.user_detail import *
from projectx_app.models.vendor import *


class MedicalCheck(models.Model):
    myrequest = models.ForeignKey(MyRequest, on_delete=models.CASCADE, related_name='medical_my_request', null=True, blank=True)
    vendor = models.ForeignKey(CompanyVendor, on_delete=models.CASCADE, related_name='medical_check_vendor', null=True, blank=True)
    vendor_email = models.CharField(max_length=100, null=True, blank=True, verbose_name='Vendor Email')
    due_date = models.CharField(max_length=10, null=True, blank=True, verbose_name='Due Date')
    attached_template = models.FileField(blank=True, null=True, verbose_name='Attached Template')
    comments = models.TextField(blank=True, null=True, verbose_name='Comments')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medicalcheck_owner', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.myrequest.applicant.user.email

    class Meta:
        verbose_name = "Medical Check"
        verbose_name_plural = "Medical Checks"
