from django import forms
from PIL import Image
from projectx_app.models.user import User
from projectx_app.models.user_detail import *
from projectx_app.models.company import *
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from .common_fn import get_initial_values

class CompanySetUpForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        initial_country_exist, initial_country, initial_country_code_exist, initial_countrycode = get_initial_values()
        super(CompanySetUpForm, self).__init__(*args, **kwargs)

        self.fields['x'].required = False
        self.fields['y'].required = False
        self.fields['width'].required = False
        self.fields['height'].required = False

        self.fields['logo_image'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['country'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['country'].initial = initial_country.id if initial_country_exist else ""
        self.fields['company_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['address'].widget.attrs['class'] = 'form-control r-0 light s-12'

        self.fields['finance_user_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['finance_email'].widget.attrs['class'] = 'form-control r-0 light s-12'

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
        self.fields['contract_status'].initial = True

        self.fields['rpo_provider'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['rpo'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['contract_start_date'].widget.attrs['autocomplete'] = "off"
        self.fields['contract_end_date'].widget.attrs['autocomplete'] = "off"

    class Meta:
        model = SystemCompanySetup
        fields = ('__all__')

    def save(self, request, commit=True):
        instance = super(CompanySetUpForm, self).save(commit=False)
        email = self.cleaned_data.get('email')
        company_admin = self.cleaned_data.get('company_admin')
        phone_no = self.cleaned_data.get('phone_no') if self.cleaned_data.get('phone_no') else ''

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')

        if ' ' in company_admin:
            first_name, last_name = company_admin.split(' ', 1)
        else:
            first_name = company_admin
            last_name = ''

        if not self.instance.pk:
            # create
            if commit:
                password = User.objects.make_random_password()
                user = User.objects.create(first_name = first_name, last_name = last_name, mobile_number = phone_no, email = email, password=make_password(password), user_type = 2)
                instance.user = user

                try:
                    companyuser = SystemCompanySetup.objects.last()
                except:
                    companyuser = None

                try:
                    company_id = int(companyuser.company_id[2]) + 1
                except:
                    company_id = 1

                instance.company_id = '22'+str(company_id)
                instance.save()

                company_user = CompanyUser.objects.create(user = user, company = instance, owner = request.user)

                html_message = "Dear Administrator,"+"<br><br>Welcome to Plat X. We are delighted to have you onboard !<br><br>Please find your first time login credentials :<br>"+"Your email: "+email+"<br>Password: "+password+" <br>After your first login please change your password.<br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
                email_message = EmailMessage('Password Information', html_message, settings.EMAIL_HOST_USER, [],[email])
                email_message.content_subtype = "html"
                email_message.send()
        else:
            # update
            if commit:
                # todo - this will work till the user's email is not editable
                try:
                    user = User.objects.get(email = email)
                except:
                    user = None

                if user:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.mobile_number = phone_no
                    user.save()
                instance.save()

        if instance.logo_image:
            image = Image.open(instance.logo_image)

        if x and y and width and height:
            cropped_image = image.crop((x, y, width+x, height+y))
            resized_image = cropped_image.resize((80, 80), Image.ANTIALIAS)
            resized_image.save('projectx_app/static/img/profile_files/'+instance.logo_image.name)

        return instance



class CompanyUserForm(forms.ModelForm):

    STATUS = (
        (True, 'Active'),
        (False, 'InActive')
    )

    COMPANY_USER_CHOICES = (
        (2, 'Admin'),
        (6, 'Recruiter'),
        (7, 'Medical Officer'),
        (8, 'Hiring Manager'),
    )

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=40)    
    mobile_number = forms.CharField(max_length=30, required=False)
    status = forms.ChoiceField(choices = STATUS)
    user_type = forms.ChoiceField(choices = COMPANY_USER_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        company_user = super(CompanyUserForm, self).__init__(*args, **kwargs)
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
        model = CompanyUser
        fields = ('__all__')

    def save(self, request, commit=True):
        instance = super(CompanyUserForm, self).save(commit=False)
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

                html_message = "Dear "+first_name+",<br><br>Your account on Plat X is now active, please find your first time login credentials :<br><br>Username: "+email+"<br>Password: "+password+" <br>After your first login please change your password.<br><br>If you have any questions please drop me an email or call me.<br><br>Thanks,<br>Company Admin<br>"

                email_message = EmailMessage('Password Information', html_message, settings.EMAIL_HOST_USER, [],[email])
                email_message.content_subtype = "html"
                email_message.send()


                instance.user = user
                instance.owner = request.user
                instance.company = company
                instance.user.save()
                instance.save()
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

