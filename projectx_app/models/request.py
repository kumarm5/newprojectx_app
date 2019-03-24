from django.db import models
from django.conf import settings
from projectx_app.models.master import *
from projectx_app.models.user_detail import *
from projectx_app.models.onboarding import *
from projectx_app.models.applicant import *
from projectx_app.models.company import *


STATUS = (
    (True, 'Active'),
    (False, 'Inactive'),
)

PROGRESS_STATUS = (
    ('Assigned','Assigned'),
    ('In Progress','In Progress'),
    ('Completed','Completed'),
)

RESULT = (
    ('All Clear','All Clear'),
    ('Request can not be processed','Request can not be processed'),
    ('Document Requested again','Document Requested again'),
    ('Minor Issues','Minor Issues'),
    ('Serious medical condition','Serious medical condition'),
    ('Failed','Failed'),
)

HIRING_MANAGER_STATUS = (
    ('Approve','Approve'),
    ('Reject','Reject'),
)

CMO_MANAGER_STATUS = (
    ('Approve','Approve'),
    ('Reject','Reject'),
)

class MyRequest(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='user_request')
    company = models.ForeignKey(SystemCompanySetup, on_delete=models.CASCADE, null=True, blank=True)
    co_onboarding_type = models.ForeignKey(CoOnboardingType, on_delete=models.CASCADE, null=True, blank=True)
    job_id = models.CharField(max_length=256, null=True, blank=True, verbose_name='Job Id')
    position_id = models.CharField(max_length=256, null=True, blank=True, verbose_name='Position Id')
    hiring_manager = models.CharField(max_length=256, null=True, blank=True, verbose_name='Hiring Manager') #not in use now
    hiring_manager_user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='myrequest_hiring_manager', null=True, blank=True, verbose_name='Hiring Manager User')
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='recruiter')
    request_status = models.BooleanField(choices=STATUS, max_length=256, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_created_by', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.applicant.user.email

    class Meta:
        verbose_name = 'My Request'
        verbose_name_plural = 'My Requests'


class MyRequestTasksInfo(models.Model):
    myrequest = models.ForeignKey(MyRequest, on_delete=models.CASCADE, related_name='my_requestinfo', null=True, blank=True)
    task = models.ForeignKey(CoOnboardingTask, on_delete=models.CASCADE, related_name='requestinfo_task', null=True, blank=True)
    co_onboarding_type = models.ForeignKey(CoOnboardingType, on_delete=models.CASCADE, related_name='requestinfo_onboarding_type', null=True, blank=True)
    company = models.ForeignKey(SystemCompanySetup, on_delete=models.CASCADE, null=True, blank=True)
    step_id = models.CharField(max_length=256, null=True, blank=True)
    medical_cmo_user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, verbose_name='Medical CMO User', related_name='request_medical_cmo_user', blank=True, null=True)
    task_name = models.CharField(max_length=256, verbose_name='Task Name', null=True, blank=True)
    vendor = models.ForeignKey(CompanyVendor, on_delete=models.CASCADE, related_name='requestinfo_vendor', null=True, blank=True)
    vendor_user = models.ForeignKey(CompanyVendor, on_delete=models.CASCADE, related_name='requestinfo_vendor_user', null=True, blank=True)
    request_due_date = models.CharField(max_length=256, null=True, blank=True, verbose_name='requestinfo_due_date')
    progress_status = models.CharField(choices=PROGRESS_STATUS, max_length=100, blank=True, null=True)
    result = models.CharField(default='Pending', choices=RESULT, max_length=100, blank=True, null=True)
    file_name = models.FileField(upload_to='vendor_files/', blank=True, null=True, verbose_name='File Name')
    comments = models.TextField(blank=True, null=True, verbose_name='Comments')
    result_comment = models.TextField(blank=True, null=True, verbose_name='Result Comments')
    hiring_manager_comment = models.TextField(blank=True, null=True, verbose_name='Hiring Manager Comments')
    hiring_manager_status = models.CharField(choices=HIRING_MANAGER_STATUS, max_length=100, blank=True, null=True)
    cmo_manager_comment = models.TextField(blank=True, null=True, verbose_name='CMO Manager Comments')
    cmo_manager_status = models.CharField(choices=CMO_MANAGER_STATUS, max_length=100, blank=True, null=True)
    is_vendor_action = models.BooleanField(blank=True, null=True, default=False, verbose_name='Is Vendor Actioned')
    is_cmo_action = models.BooleanField(blank=True, null=True, default=False, verbose_name='Is CMO Actioned')
    is_hiring_manager_action = models.BooleanField(blank=True, null=True, default=False, verbose_name='Is Hiring Manager Actioned')
    send_to_candidate = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requestinfo_owner', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.task_name

    class Meta:
        verbose_name = 'My Request Task Info'
        verbose_name_plural = 'My Request Task Infos'


class MyRequestTaskBGV(models.Model):
    myrequest_tasks_info = models.ForeignKey(MyRequestTasksInfo, on_delete=models.CASCADE, related_name='myrequest_bgv_task')
    document = models.ForeignKey(DocumentTypeName, on_delete=models.CASCADE, related_name='myrequest_bgv_document')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.myrequest_tasks_info.task.task_name

    class Meta:
        verbose_name = 'My Request BGV'
        verbose_name_plural = 'My Request BGVs'


class MyRequestTaskRefCheck(models.Model):
    myrequest_tasks_info = models.ForeignKey(MyRequestTasksInfo, on_delete=models.CASCADE, related_name='myrequest_ref_task')
    reference_check = models.ForeignKey(SysRefCheck, on_delete=models.CASCADE, related_name='myrequest_sys_ref')
    no_of_references = models.CharField(max_length=5, verbose_name='Number of Reference')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.myrequest_tasks_info.task.task_name

    class Meta:
        verbose_name = 'My Request REF'
        verbose_name_plural = 'My Request REFs'


class MyRequestTaskHrForm(models.Model):
    myrequest_tasks_info = models.ForeignKey(MyRequestTasksInfo, on_delete=models.CASCADE, related_name='myrequest_hr_task')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='myrequest_hr_templates')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.myrequest_tasks_info.task.task_name

    class Meta:
        verbose_name = 'My Request HR'
        verbose_name_plural = 'My Request HRs'


class MyRequestTaskMedicalForm(models.Model):
    myrequest_tasks_info = models.ForeignKey(MyRequestTasksInfo, on_delete=models.CASCADE, related_name='myrequest_medical_task')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='myrequest_medical_templates')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return ''

    class Meta:
        verbose_name = 'My Request Medical'
        verbose_name_plural = 'My Request Medicals'
