from django import forms
from projectx_app.models.user import User
from projectx_app.models.user_detail import *
from projectx_app.models.rpo import *
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from .common_fn import get_initial_values

class SysRpoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop('user' , None)
        initial_country_exist, initial_country, initial_country_code_exist, initial_countrycode = get_initial_values()
        super(SysRpoForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['country'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['country'].initial = initial_country.id if initial_country_exist else ""
        self.fields['rpo_company_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['address'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['phone_no'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['company_admin'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['country_code'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['country_code'].initial = initial_countrycode.id if initial_country_code_exist else ""
        self.fields['area_code'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['number'].widget.attrs['class'] = 'form-control r-0 light s-12'

        self.fields['email'].widget.attrs['class'] = 'form-control r-0 light s-12'

        self.fields['annual_contract_value'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['contract_start_date'].widget.attrs['class'] = 'form-control date-picker r-0 light s-12'
        self.fields['contract_end_date'].widget.attrs['class'] = 'form-control date-picker r-0 light s-12'
        self.fields['upload_contract'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['tax_number'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['contract_status'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['contract_start_date'].widget.attrs['autocomplete'] = "off"
        self.fields['contract_end_date'].widget.attrs['autocomplete'] = "off"

    class Meta:
        model = SysRpo
        fields = ('__all__')

    def save(self, request, commit=True):

        rpo = super(SysRpoForm, self).save(commit=False)
        email = self.cleaned_data.get('email')
        company_admin = self.cleaned_data.get('company_admin')
        phone_no = self.cleaned_data.get('phone_no') if self.cleaned_data.get('phone_no') else ''

        if ' ' in company_admin:
            first_name, last_name = company_admin.split(' ', 1)
        else:
            first_name = company_admin
            last_name = ''

        if not self.instance.pk:
            # create
            if commit:
                password = User.objects.make_random_password()
                user = User.objects.create(first_name = first_name, last_name = last_name, email = email, mobile_number = phone_no, password = make_password(password), user_type = 5)

                rpo.user = user

                try:
                    sysrpo = SysRpo_Setup.objects.last()
                except:
                    sysrpo = None

                try:
                    rpo_id = int(sysrpo.rpo_id[2]) + 1
                except:
                    rpo_id = 1

                rpo.rpo_id = '33'+str(rpo_id)
                rpo.save()

                rpo_user = RPOUser.objects.create(user = user, rpo = rpo, owner = request.user)

                html_message = "Dear Administrator,"+"<br><br>Welcome to Plat X. We are delighted to have you onboard !<br><br>Please find your first time login credentials :<br>"+"Your email: "+email+"<br>Password: "+password+" <br>After your first login please change your password.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
                email_message = EmailMessage('Password Information', html_message, settings.EMAIL_HOST_USER, [],[email])
                email_message.content_subtype = "html"
                email_message.send()
        else:
            # update
            if commit:
                rpo.save()

        return rpo


class RPOUserForm(forms.ModelForm):

    STATUS = (
        (True, 'Active'),
        (False, 'InActive')
    )

    RPO_USER_CHOICES = (
        (5, 'Admin'),
        (9, 'User'),
    )

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=40)    
    mobile_number = forms.CharField(max_length=30, required=False)
    status = forms.ChoiceField(choices = STATUS)
    user_type = forms.ChoiceField(choices = RPO_USER_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        rpo_user = super(RPOUserForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['first_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['last_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['email'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['status'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['mobile_number'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['user_type'].widget.attrs['class'] = 'form-control r-0 light s-12'

        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['status'].initial = self.instance.user.is_active
            self.fields['mobile_number'].initial = self.instance.user.mobile_number
            self.fields['user_type'].initial = self.instance.user.user_type

    class Meta:
        model = RPOUser
        fields = ('__all__')


    def save(self, request, commit=True):
        instance = super(RPOUserForm, self).save(commit=False)
        rpouser = None

        try:
            rpouser = RPOUser.objects.get(user = request.user)
        except:
            rpouser = None

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        mobile_number = self.cleaned_data.get('mobile_number')
        status = self.cleaned_data.get('status')
        user_type = int(self.cleaned_data.get('user_type'))

        if status == 'True':
            status = True
        else:
            status = False

        if not self.instance.pk:
            # create
            if commit:
                password = User.objects.make_random_password()
                user = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = make_password(password), user_type = user_type, mobile_number = mobile_number, is_active = status)

                instance.user = user
                instance.rpo = rpouser.rpo
                instance.owner = request.user
                instance.user.save()
                instance.save()

                html_message = "Dear "+first_name+", <br><br>Welcome to Plat X. We are delighted to have you onboard !<br><br>Please find your first time login credentials :<br>"+"Your email: "+email+"<br>Password: "+password+" <br>After your first login please change your password.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
                email_message = EmailMessage('Password Information', html_message, settings.EMAIL_HOST_USER, [],[email])
                email_message.content_subtype = "html"
                email_message.send()
        else:
            # update
            if commit:
                instance.user.first_name = first_name
                instance.user.last_name = last_name
                instance.user.email = email
                instance.user.mobile_number = mobile_number
                instance.user.user_type = user_type
                instance.user.is_active = status
                instance.rpo = rpouser.rpo
                instance.user.save()
                instance.save()

        return instance
