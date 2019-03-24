from django import forms
from projectx_app.models.user import User
from projectx_app.models.reimbursement import Reimbursement, ReimbursementDocument
from projectx_app.models.request import *
from projectx_app.models.company import *
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage


class ReimbursementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user =  kwargs.pop('user', None)

        company = None
        co_onboarding_type = None

        super(ReimbursementForm, self).__init__(*args, **kwargs)
        self.fields['system_company_setup'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['co_onboarding'].widget.attrs['class'] = 'form-control r-0 light s-12'        
        myrequest = MyRequest.objects.filter(applicant__user = user).values_list('company', 'co_onboarding_type')

        if myrequest:
            company = myrequest[0][0]
            co_onboarding_type = myrequest[0][1]

        self.fields['system_company_setup'].queryset = SystemCompanySetup.objects.filter(id = company)
        self.fields['co_onboarding'].queryset = CoOnboardingType.objects.filter(id = co_onboarding_type)

        self.fields['system_company_setup'].initial = company
        self.fields['co_onboarding'].initial = co_onboarding_type

    class Meta:
        model = Reimbursement
        fields = ('__all__')

    def save(self, request, commit=True):
        instance = super(ReimbursementForm, self).save(commit=True)
        file_name_path = []
        fs = FileSystemStorage()
        fs.location = fs.location+'/media/'

        if request.FILES:
            for f in request.FILES.getlist('upload_file'):
                obj = ReimbursementDocument.objects.create(reimbursement = instance, document_file = f)
                filename = fs.save(obj.document_file.name, obj.document_file)
                filename_path = 'media/'+filename
                file_name_path.append(filename_path)

        if instance.system_company_setup.finance_email and instance.system_company_setup.finance_user_name:
            html_message = "Dear "+instance.system_company_setup.finance_user_name+", <br><br>Welcome to Plat X. Reimbursement file is uploaded for you. Please check the files !<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
            email_message = EmailMessage('Reimbursement', html_message, settings.EMAIL_HOST_USER, [],[instance.system_company_setup.finance_email])
            email_message.content_subtype = "html"

            if len(file_name_path) != 0:
                for filenamepath in file_name_path:
                    email_message.attach_file(filenamepath)

            email_message.send()


        myrequest = MyRequest.objects.filter(applicant__user = request.user).last()

        if myrequest.recruiter:
            html_message = "Dear "+myrequest.recruiter.first_name+", <br><br>Welcome to Plat X. Reimbursement file is uploaded for you. Please check the files !<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
            email_message = EmailMessage('Reimbursement', html_message, settings.EMAIL_HOST_USER, [],[myrequest.recruiter.email])
            email_message.content_subtype = "html"

            if len(file_name_path) != 0:
                for filenamepath in file_name_path:
                    email_message.attach_file(filenamepath)

            email_message.send()

        # instance.co_onboarding.company
            # if request.FILES:
            #     fs = FileSystemStorage()
            #     for f in request.FILES.getlist('upload_file'):
            #         import pdb
            #         pdb.set_trace()
            #         filename = fs.save(f.name, f)
            #         uploaded_file_url = fs.url(filename)
            #         email_message.attach_file(uploaded_file_url)

        return instance
