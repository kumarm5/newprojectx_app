from django.db import models
from django.conf import settings
from projectx_app.models.user import User
from projectx_app.models.company import SystemCompanySetup
from projectx_app.models.onboarding import CoOnboardingType
from projectx_app.models.applicant import Applicant

class Reimbursement(models.Model):
    '''
        'owner' is the 'applicant' who is going the fill the form for reimbursement
    '''
    system_company_setup = models.ForeignKey(SystemCompanySetup, related_name='company_reimbursement', on_delete=models.CASCADE)
    co_onboarding = models.ForeignKey(CoOnboardingType, related_name='co_onboarding_reimbursement', on_delete=models.CASCADE)
    # upload_file = models.FileField(null=True, blank=True, verbose_name='Upload File')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reimbursement_owner', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.owner.first_name

    class Meta:
        verbose_name = "Reimbursement"
        verbose_name_plural = "Reimbursements"


class ReimbursementDocument(models.Model):
    reimbursement = models.ForeignKey(Reimbursement, related_name='reimbursement_file', on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='my-reimbursement/', verbose_name='Document File')

    def __str__(self):
        return str(self.reimbursement.applicant.user.first_name) if self.reimbursement.applicant.user.first_name else ''
    
    class Meta:
        verbose_name = "Reimbursement Document"
        verbose_name_plural = "Reimbursement Documents"

