from django import forms
from projectx_app.models.user import User
from projectx_app.models.company import *
from projectx_app.models.user_detail import *
from projectx_app.models.medical_check import *
from projectx_app.models.vendor import *
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage


class MedicalCheckUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user =  kwargs.pop('user')
        
        super(MedicalCheckUpForm, self).__init__(*args, **kwargs)
        self.fields['myrequest'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['vendor'].widget.attrs['class'] = 'form-control r-0 light s-12'

        try:
            company_user = CompanyUser.objects.get(user = user)
        except:
            company_user = None
        
        if company_user:
            self.fields['vendor'].queryset = CompanyVendor.objects.filter(
                sys_vendor_type__type_description__icontains = 'Medical',
                company = company_user.company
            )
        else:
            self.fields['vendor'].queryset = CompanyVendor.objects.filter(
                sys_vendor_type__type_description__icontains = 'Medical'
            )

        self.fields['vendor_email'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['due_date'].widget.attrs['class'] = 'form-control r-0 light s-12 date-picker'
        self.fields['attached_template'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['comments'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['due_date'].widget.attrs['autocomplete'] = "off"

    class Meta:
        model = MedicalCheck
        fields = ('__all__')
