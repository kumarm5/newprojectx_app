from django.db import models
from django.conf import settings
from projectx_app.models.user import User
from projectx_app.models.master import *
from projectx_app.models.company import *
from projectx_app.models.user_detail import *


STATUS = (
    (True, 'Active'),
    (False, 'Inactive'),
)

class Template(models.Model):
    company = models.ForeignKey(SystemCompanySetup, on_delete=models.CASCADE, related_name='template_company')
    template_name = models.CharField(max_length=100)
    template_type = models.ForeignKey(TemplateType, on_delete=models.CASCADE, related_name='template_type', blank=True, null=True)
    template_status = models.BooleanField(choices=STATUS, max_length=20, blank=True, null=True)
    template_doc = models.FileField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='template_owner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False, blank=True, null=True, verbose_name='Delete Status')

    def __str__(self):
        return self.template_name

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"