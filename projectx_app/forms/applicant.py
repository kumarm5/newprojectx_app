from django import forms
from projectx_app.models.user import User
from projectx_app.models.applicant import *
from projectx_app.models.user_detail import *
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
import socket


class ApplicantForm(forms.ModelForm):

    STATUS = (
        (True, 'Active'),
        (False, 'InActive')
    )

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=40)
    phone_no = forms.CharField(max_length=30, required=False)
    status = forms.ChoiceField(choices = STATUS)

    def __init__(self, *args, **kwargs):
        applicant = super(ApplicantForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['first_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['last_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['email'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['status'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['location'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['ip_address'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['phone_no'].widget.attrs['class'] = 'form-control r-0 light s-12'

        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['status'].initial = self.instance.user.is_active
            self.fields['phone_no'].initial = self.instance.user.mobile_number

    class Meta:
        model = Applicant
        fields = ('__all__')

    def save(self, commit=True):
        instance = super(ApplicantForm, self).save(commit=False)

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        phone_no = self.cleaned_data.get('phone_no')
        status = self.cleaned_data.get('status')

        if status == 'True':
            status = True
        else:
            status = False            

        if not self.instance.pk:
            # create
            if commit:
                password = User.objects.make_random_password()
                user = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = make_password(password), user_type = 1, mobile_number = phone_no, is_active = status)
                hostname = socket.gethostname()
                instance.ip_address = socket.gethostbyname(hostname)
                instance.user_id = user.id
                instance.save()

                html_message = "Dear Applicant,"+"<br><br>Welcome to Plat X. We are delighted to have you onboard !<br><br>Please find your first time login credentials :<br>"+"Your email: "+user.email+"<br>Password: "+password+" <br>After your first login please change your password.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
                email_message = EmailMessage('Password Information', html_message, settings.EMAIL_HOST_USER, [],[user.email])
                email_message.content_subtype = "html"
                email_message.send()
        else:
            # update
            if commit:
                instance.user.first_name = first_name
                instance.user.last_name = last_name
                instance.user.email = email
                instance.user.mobile_number = phone_no
                instance.user.is_active = status
                instance.user.save()
                instance.save()

        return instance
