from django.db import models
from django.conf import settings
from projectx_app.models.master import *
from projectx_app.models.request import *
from projectx_app.models.template import *
from projectx_app.models.user_detail import *
from projectx_app.models.onboarding import *
from projectx_app.models.company import *


class MyRequestTasks(models.Model):
    myrequest = models.ForeignKey(MyRequest, on_delete=models.CASCADE, related_name='my_request', null=True, blank=True)
    task = models.ForeignKey(MyRequestTasksInfo, on_delete=models.CASCADE, related_name='request_task', null=True, blank=True)
    co_onboarding_type = models.ForeignKey(CoOnboardingType, on_delete=models.CASCADE, related_name='request_onboarding_type', null=True, blank=True)
    step_id = models.CharField(max_length=256, null=True, blank=True)
    task_name = models.CharField(max_length=256, verbose_name='Task Name', null=True, blank=True)
    vendor = models.ForeignKey(CompanyVendor, on_delete=models.CASCADE, related_name='my_request_vendor', null=True, blank=True)
    cmo_user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, verbose_name='CMO User', related_name='task_cmo_user', blank=True, null=True)
    mark_complete = models.BooleanField(default=False, verbose_name='Mark Complete')
    request_due_date = models.CharField(max_length=256, null=True, blank=True, verbose_name='request_due_date')
    send_to_candidate = models.BooleanField(default=False)

    def __str__(self):
        return self.task.task_name

    class Meta:
        verbose_name = 'My Request Task'
        verbose_name_plural = 'My Request Tasks'


class MyRequestTasksBgvDocs(models.Model):
    myrequest_task = models.ForeignKey(MyRequestTasks, on_delete=models.CASCADE, related_name='my_request_task')
    document = models.ForeignKey(DocumentTypeName, on_delete=models.CASCADE, related_name='my_request_document')
    document_file = models.FileField(blank=True, null=True, verbose_name='Document Name')
    mark_complete = models.BooleanField(blank=True, null=True, verbose_name='Request Mark Complete')
    not_applicable = models.BooleanField(blank=True, null=True, verbose_name='Request Not Applicable')

    def __str__(self):
        return self.document.document_name

    class Meta:
        verbose_name = 'My Request Document'
        verbose_name_plural = 'My Request Documents'



class MyRequestTasksRefDocs(models.Model):
    myrequest_task = models.ForeignKey(MyRequestTasks, on_delete=models.CASCADE, related_name='my_ref_task')
    reference = models.ForeignKey(SysRefCheck, on_delete=models.CASCADE, related_name='my_reference')
    ref_name = models.CharField(max_length=256 ,blank=True, null=True)
    ref_organisation = models.CharField(max_length=256 ,blank=True, null=True)
    ref_office_email = models.CharField(max_length=256 ,blank=True, null=True)
    ref_relation = models.CharField(max_length=256 ,blank=True, null=True)
    ref_phone = models.CharField(max_length=256 ,blank=True, null=True)
    row_index = models.CharField(max_length=256 ,blank=True, null=True)
    mark_complete = models.BooleanField(default=False, verbose_name='Mark Complete')
    not_applicable = models.BooleanField(blank=True, null=True, verbose_name='Request Not Applicable')

    class Meta:
        verbose_name = 'My Request Reference Detail'
        verbose_name_plural = 'My Request Reference Details'


class MyRequestTasksHrDocs(models.Model):
    myrequest_task = models.ForeignKey(MyRequestTasks, on_delete=models.CASCADE, related_name='my_hr_task')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='my_hr_template', blank=True, null=True)
    document_name = models.FileField(blank=True, null=True, verbose_name='Document Name')
    mark_complete = models.BooleanField(blank=True, null=True, verbose_name='Request Mark Complete')
    not_applicable = models.BooleanField(blank=True, null=True, verbose_name='Request Not Applicable')

    def __str__(self):
        return self.template.template_name

    class Meta:
        verbose_name = 'My Request Hr Document'
        verbose_name_plural = 'My Request Hr Documents'


class MyRequestTasksMedicalDocs(models.Model):
    myrequest_task = models.ForeignKey(MyRequestTasks, on_delete=models.CASCADE, related_name='my_medical_task')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='my_medical_template', blank=True, null=True)
    document_name = models.FileField(blank=True, null=True, verbose_name='Document Name')
    mark_complete = models.BooleanField(blank=True, null=True, verbose_name='Request Mark Complete')
    not_applicable = models.BooleanField(blank=True, null=True, verbose_name='Request Not Applicable')

    def __str__(self):
        return ''

    class Meta:
        verbose_name = 'My Request Medical Document'
        verbose_name_plural = 'My Request Medical Documents'

