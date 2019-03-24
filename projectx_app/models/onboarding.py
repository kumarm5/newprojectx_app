from django.db import models
from django.conf import settings
from projectx_app.models.user import User
from projectx_app.models.master import *
from projectx_app.models.template import *
from projectx_app.models.user_detail import *
from projectx_app.models.vendor import *
from projectx_app.models.company import *


class CoOnboardingType(models.Model):
    co_onboarding_type_name = models.CharField(max_length=256, verbose_name='On-Boarding Type Name')
    company = models.ForeignKey(SystemCompanySetup, on_delete=models.CASCADE, related_name='onboard_company')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.co_onboarding_type_name

    class Meta:
        verbose_name = "Company Onboarding Type"
        verbose_name_plural = "Company Onboarding Types"


class CoOnboardingTask(models.Model):
    step_id = models.CharField(max_length=256, verbose_name='Step Id', null=True, blank=True)
    task_name = models.CharField(max_length=256, verbose_name='Task Name')
    vendor = models.ForeignKey(CompanyVendor, on_delete=models.CASCADE, related_name='onboarding_vendor', blank=True, null=True)
    co_onboarding_type = models.ForeignKey(CoOnboardingType, on_delete=models.CASCADE, related_name='onboarding_type')
    comment = models.TextField(verbose_name='Comment')
    due_date = models.CharField(max_length=100, verbose_name='Due Date')
    medical_cmo_user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, verbose_name='Medical CMO User', related_name='medical_cmo_user', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    send_to_candidate = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name

    class Meta:
        verbose_name = 'Company On-Boarding Task'
        verbose_name_plural = 'Company On-Boarding Tasks'


class CoOnboardingTaskBGV(models.Model):
    co_onboarding_task = models.ForeignKey(CoOnboardingTask, on_delete=models.CASCADE, related_name='onboarding_bgv_task')
    document = models.ForeignKey(DocumentTypeName, on_delete=models.CASCADE, related_name='onboarding_bgv_document')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.co_onboarding_task.task_name

    class Meta:
        verbose_name = 'Company On-Boarding BGV'
        verbose_name_plural = 'Company On-Boarding BGVs'


class CoOnboardingTaskRefCheck(models.Model):
    onboarding_ref_task = models.ForeignKey(CoOnboardingTask, on_delete=models.CASCADE, related_name='onboarding_ref_task')
    reference_check = models.ForeignKey(SysRefCheck, on_delete=models.CASCADE, related_name='onboarding_sys_ref')
    no_of_references = models.CharField(max_length=5, verbose_name='Number of Reference')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.onboarding_ref_task.task_name

    class Meta:
        verbose_name = 'Company On-Boarding REF'
        verbose_name_plural = 'Company On-Boarding REFs'


class CoOnboardingTaskHrForm(models.Model):
    onboarding_hr_task = models.ForeignKey(CoOnboardingTask, on_delete=models.CASCADE, related_name='onboarding_hr_task')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='onboarding_hr_templates')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.onboarding_hr_task.task_name

    class Meta:
        verbose_name = 'Company On-Boarding HR'
        verbose_name_plural = 'Company On-Boarding HRs'


class CoOnboardingTaskMedicalForm(models.Model):
    onboarding_medical_task = models.ForeignKey(CoOnboardingTask, on_delete=models.CASCADE, related_name='onboarding_medical_task')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='onboarding_medical_templates')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.onboarding_hr_task.task_name

    class Meta:
        verbose_name = 'Company On-Boarding Medical'
        verbose_name_plural = 'Company On-Boarding Medicals'
