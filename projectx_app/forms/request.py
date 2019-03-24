from django import forms
from projectx_app.models.user import User
from projectx_app.models.request import *
from projectx_app.models.user_detail import *
from projectx_app.models.task import *
from django.conf import settings
from django.contrib.auth.hashers import make_password
import datetime
from django.core.mail import EmailMessage

class RequestApplicantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RequestApplicantForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['last_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['email'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['mobile_number'].widget.attrs['class'] = 'form-control r-0 light s-12'

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile_number',)

    def save(self, commit=True):
        instance = super(RequestApplicantForm, self).save(commit=False)
        instance.password = make_password('applicant@123')
        instance.user_type = 1
        instance.save()
        return instance


class MyRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyRequestForm, self).__init__(*args, **kwargs)
        self.fields['applicant'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['company'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['co_onboarding_type'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['job_id'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['position_id'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['hiring_manager'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['recruiter'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['request_status'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['hiring_manager'].widget.attrs['class'] = 'form-control r-0 light s-12'

    class Meta:
        model = MyRequest
        fields = ('__all__')


class MyRequestTasksInfoForm(forms.ModelForm):
    current_date = forms.CharField(required = False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        instance = super(MyRequestTasksInfoForm, self).__init__(*args, **kwargs)
        task_name = kwargs['instance'].task_name
        is_vendor_action = kwargs['instance'].is_vendor_action

        GENERIC_RESULT = (
            ('All Clear','All Clear'),
            ('Request can not be processed','Request can not be processed'),
            ('Document Requested again','Document Requested again'),            
            ('Failed','Failed'),
        )


        FORM_RESULT = (
            ('', '---------'),
            ('All Clear','All Clear'),
            ('Document Requested again','Document Requested again'),
        )

        CMO_RESULT = (
            ('', '---------'),
            ('All Clear','All Clear'),
            ('Minor Issues','Minor Issues'),
            ('Serious medical condition','Serious medical condition'),
        )

        self.fields['task'].required = False
        self.fields['myrequest'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['task'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['co_onboarding_type'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['company'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['step_id'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['task_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['vendor'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['request_due_date'].widget.attrs['class'] = 'form-control r-0 light s-12'

        self.fields['progress_status'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['result'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['file_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['result_comment'].widget.attrs['class'] = 'form-control r-0 light s-12'

        if task_name == "Employment Forms":
            self.fields['result'].choices = FORM_RESULT
        elif task_name == "Medical Check":
            self.fields['result'].choices = CMO_RESULT
        else:
            self.fields['result'].choices = GENERIC_RESULT

        if user.user_type == 4: # if the logged in user is case worker            
            if kwargs['instance'].is_cmo_action == True or kwargs['instance'].is_hiring_manager_action == True:
                self.fields['progress_status'].widget.attrs['class'] = 'form-control r-0 light s-12 disabled'
                self.fields['result'].widget.attrs['class'] = 'form-control r-0 light s-12 disabled'
                self.fields['file_name'].widget.attrs['class'] = 'form-control r-0 light s-12 disabled'
                self.fields['result_comment'].widget.attrs['class'] = 'form-control r-0 light s-12 disabled'

        if user.user_type == 8: # if the logged in user is hiring manager
            self.fields['progress_status'].widget.attrs['class'] = 'form-control r-0 light s-12 disabled'
            self.fields['result'].widget.attrs['class'] = 'form-control r-0 light s-12 disabled'
            self.fields['file_name'].widget.attrs['class'] = 'form-control r-0 light s-12 disabled'
            self.fields['result_comment'].widget.attrs['class'] = 'form-control r-0 light s-12 disabled'
            self.fields['hiring_manager_comment'].widget.attrs['class'] = 'form-control r-0 light s-12'
            self.fields['hiring_manager_status'].widget.attrs['class'] = 'form-control r-0 light s-12'

        if user.user_type == 7: # if the logged in user is CMO
            if task_name == "Medical Check":
                self.fields['result'].choices = CMO_RESULT
            if is_vendor_action == False:
                self.fields['result'].widget.attrs['class'] = 'form-control r-0 light s-12'
            else:
                self.fields['progress_status'].widget.attrs['class'] = 'form-control r-0 light s-12 disabled'
                self.fields['result'].widget.attrs['class'] = 'form-control r-0 light s-12 disabled'
                self.fields['file_name'].widget.attrs['class'] = 'form-control r-0 light s-12 disabled'
                self.fields['result_comment'].widget.attrs['class'] = 'form-control r-0 light s-12 disabled'
            self.fields['cmo_manager_comment'].widget.attrs['class'] = 'form-control r-0 light s-12'
            self.fields['cmo_manager_status'].widget.attrs['class'] = 'form-control r-0 light s-12'

        self.fields['comments'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['vendor'].required = False
        self.fields['vendor_user'].required = False

        date = datetime.datetime.utcnow()

        self.fields['current_date'].initial = date

    class Meta:
        model = MyRequestTasksInfo
        fields = ('__all__')

    def save(self, request, commit=True):
        instance = super(MyRequestTasksInfoForm, self).save(commit=False)

        result = self.cleaned_data.get('result')
        progress_status = self.cleaned_data.get('progress_status')
        step_id = self.cleaned_data.get('step_id')

        if instance.is_vendor_action == False and progress_status == 'Completed' and result == 'Request can not be processed' or result == 'Failed' and step_id == '1' or step_id == '2':            
            html_message = "Dear "+instance.myrequest.hiring_manager_user.user.first_name+", <br><br>We are sending this email to inform you that the task is assigned to you. Please take appropriate action.<br><br>Cheers,<br>Team XYZ<br>"
            email_message = EmailMessage('Failed Task', html_message, settings.EMAIL_HOST_USER, [],[instance.myrequest.hiring_manager_user.user.email])
            email_message.content_subtype = "html"
            email_message.send()

        if request.user.user_type == 8:
            html_message = "Dear "+instance.myrequest.recruiter.first_name+", <br><br>We are sending this email to inform you that the hiring manager has taken action. Please check your platformX dashboard.<br><br>Cheers,<br>Team XYZ<br>"
            email_message = EmailMessage('Hiring Manager Task Status', html_message, settings.EMAIL_HOST_USER, [],[instance.myrequest.recruiter.email])
            email_message.content_subtype = "html"
            email_message.send()

        if result == 'Document Requested again':
            MyRequestTasks.objects.filter(task = instance).update(mark_complete = False)

        # if the logged in user is vendor user (case-worker)
        if request.user.user_type == 4:
            instance.is_vendor_action = True
        # if the logged in user is CMO user
        elif request.user.user_type == 7:
            instance.is_cmo_action = True
        # if the logged in user is Hiring Manager user
        elif request.user.user_type == 8:
            instance.is_hiring_manager_action = True
        instance.save()

        return instance
