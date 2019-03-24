from django import forms
from projectx_app.models.user import User
from projectx_app.models.master import *
from projectx_app.models.vendor import *
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from .common_fn import get_initial_values

class VendorMasterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial_country_exist, initial_country, initial_country_code_exist, initial_countrycode = get_initial_values()
        instance = super(VendorMasterForm, self).__init__(*args, **kwargs)
        self.fields['vendor_company_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['country'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['country'].initial = initial_country.id if initial_country_exist else ""
        self.fields['address'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['vendor_phone'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['vendor_admin'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['admin_phone'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['country_code'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['country_code'].initial = initial_countrycode.id if initial_country_code_exist else ""
        self.fields['area_code'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['email'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['tax_number'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['service_provider_type'].widget.attrs['class'] = 'form-control r-0 light s-12'

    class Meta:
        model = VendorMaster
        fields = ('__all__')

    def save(self, request, commit=True):
        instance = super(VendorMasterForm, self).save(commit=False)

        if not self.instance.pk:
            # create
            if commit:
                instance.service_provider_type = request.POST['service_provider_type']
                instance.save()
        else:
            # update
            if commit:
                instance.service_provider_type = request.POST['service_provider_type']
                instance.save()
        return instance



class CompanyVendorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):        
        super(CompanyVendorForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['service_provider_type'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['status'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['contract_start_date'].widget.attrs['class'] = 'form-control date-picker r-0 light s-12'
        self.fields['contract_end_date'].widget.attrs['class'] = 'form-control date-picker r-0 light s-12'
        self.fields['upload_contract'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['contract_start_date'].widget.attrs['autocomplete'] = "off"
        self.fields['contract_end_date'].widget.attrs['autocomplete'] = "off"
        self.fields['sys_vendor_type'].widget.attrs['class'] = 'form-control r-0 light s-12'

    class Meta:
        model = CompanyVendor
        fields = ('__all__')

    def save(self, vendor_master_instance, request, commit=True):

        instance = super(CompanyVendorForm, self).save(commit=False)

        company = None

        if 'company_id' in request.session:
            try:
                company = SystemCompanySetup.objects.get(pk = request.session['company_id'])
            except:
                company = None
        else:
            try:
                companyuser = CompanyUser.objects.get(user = request.user)
            except:
                companyuser = None

            if companyuser:
                company = companyuser.company

        if ' ' in vendor_master_instance.vendor_admin:
            first_name, last_name = vendor_master_instance.vendor_admin.split(' ', 1)
        else:
            first_name = vendor_master_instance.vendor_admin
            last_name = ''

        if not self.instance.pk:
            # create
            if commit:
                password = User.objects.make_random_password()
                user = User.objects.create(first_name = first_name, last_name = last_name, email = vendor_master_instance.email, password = make_password(password), user_type = 3)
                instance.user = user
                instance.vendor = vendor_master_instance
                instance.company = company
                instance.user.save()
                instance.save()

                html_message = "Dear "+first_name+", <br><br>Welcome to Plat X. We are delighted to have you onboard !<br><br>Please find your first time login credentials :<br>"+"Your email: "+user.email+"<br>Password: "+password+" <br>After your first login please change your password.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
                email_message = EmailMessage('Password Information', html_message, settings.EMAIL_HOST_USER, [],[user.email])
                email_message.content_subtype = "html"
                email_message.send()
        else:
            # update
            if commit:
                instance.vendor = vendor_master_instance
                instance.company = company
                instance.save()
        return instance




class AddVendorMasterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        instance = super(AddVendorMasterForm, self).__init__(*args, **kwargs)        
        self.fields['vendor_company_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['country'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['address'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['vendor_phone'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['vendor_admin'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['admin_phone'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['country_code'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['area_code'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['email'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['tax_number'].widget.attrs['class'] = 'form-control r-0 light s-12'

        if self.instance.pk:
            self.fields['vendor_company_name'].widget.attrs['disabled'] = True
            self.fields['country'].widget.attrs['disabled'] = True
            self.fields['address'].widget.attrs['disabled'] = True
            self.fields['vendor_phone'].widget.attrs['disabled'] = True
            self.fields['vendor_admin'].widget.attrs['disabled'] = True
            self.fields['admin_phone'].widget.attrs['disabled'] = True
            self.fields['country_code'].widget.attrs['disabled'] = True
            self.fields['area_code'].widget.attrs['disabled'] = True
            self.fields['email'].widget.attrs['disabled'] = True
            self.fields['tax_number'].widget.attrs['disabled'] = True

    class Meta:
        model = VendorMaster
        fields = ('__all__')


class AddCompanyVendorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddCompanyVendorForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['owner'].required = False
        self.fields['vendor'].required = False
        self.fields['company'].required = False
        self.fields['service_provider_type'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['sys_vendor_type'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['status'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['contract_start_date'].widget.attrs['class'] = 'form-control date-picker r-0 light s-12'
        self.fields['contract_end_date'].widget.attrs['class'] = 'form-control date-picker r-0 light s-12'
        self.fields['upload_contract'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['contract_start_date'].widget.attrs['autocomplete'] = "off"
        self.fields['contract_end_date'].widget.attrs['autocomplete'] = "off"
        self.fields['service_provider_type'].widget.attrs['disabled'] = True

    class Meta:
        model = CompanyVendor
        fields = ('__all__')

    def save(self, request, user, commit=False):
        instance = super(AddCompanyVendorForm, self).save(commit=False)
        instance.service_provider_type = 'external'
        instance.user = user
        instance.save()

        html_message = "Dear "+user.first_name+", <br><br>We are glad to let you know that "+instance.company.company_name+" company has added you in their vendor list !<br><br>You can continue to use the platform as before, you will now see orders form "+instance.company.company_name+" company in your dashboard.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
        email_message = EmailMessage('You have been added as a vendor in new company', html_message, settings.EMAIL_HOST_USER, [],[user.email])
        email_message.content_subtype = "html"
        email_message.send()

        return instance


class VendorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)
        self.fields['service_provider_type'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['status'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['contract_start_date'].widget.attrs['class'] = 'form-control date-picker r-0 light s-12'
        self.fields['contract_end_date'].widget.attrs['class'] = 'form-control date-picker r-0 light s-12'
        self.fields['upload_contract'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['contract_start_date'].widget.attrs['autocomplete'] = "off"
        self.fields['contract_end_date'].widget.attrs['autocomplete'] = "off"
        self.fields['contract_start_date'].widget.attrs['required'] = True
        self.fields['contract_end_date'].widget.attrs['required'] = True
        self.fields['sys_vendor_type'].widget.attrs['class'] = 'form-control r-0 light s-12'

    class Meta:
        model = CompanyVendor
        fields = ('__all__')


class VendorUserForm(forms.ModelForm):

    STATUS = (
        (True, 'Active'),
        (False, 'InActive')
    )

    VENDOR_USER_CHOICES = (
        # (3, 'Admin'),
        (4, 'User'),
    )

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=40)    
    mobile_number = forms.CharField(max_length=30, required=False)
    status = forms.ChoiceField(choices = STATUS)
    user_type = forms.ChoiceField(choices = VENDOR_USER_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        company_user = super(VendorUserForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['owner'].required = False
        self.fields['vendor'].required = False
        self.fields['company'].required = False
        self.fields['first_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['last_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['email'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['status'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['mobile_number'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['user_type'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['sys_vendor_type'].widget.attrs['class'] = 'form-control r-0 light s-12'

        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['status'].initial = self.instance.user.is_active
            self.fields['mobile_number'].initial = self.instance.user.mobile_number
            self.fields['user_type'].initial = self.instance.user.user_type

    class Meta:
        model = CompanyVendor
        fields = ('__all__')

    def save(self, request, commit=True):
        instance = super(VendorUserForm, self).save(commit=False)
        vendor = None
        company = None

        if 'company_id' in request.session:
            try:
                vendor_user = CompanyVendor.objects.filter(company_id = request.user['company_id']).last()
            except:
                vendor_user = None
        else:
            try:
                vendor_user = CompanyVendor.objects.filter(user = request.user).last()
            except:
                vendor_user = None

        if vendor_user:
            # if vendor user has a detail
            vendor = vendor_user.vendor
            company = vendor_user.company

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
                instance.owner = request.user
                instance.vendor = vendor
                instance.company = company
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
                instance.user.save()
                instance.save()

        return instance
