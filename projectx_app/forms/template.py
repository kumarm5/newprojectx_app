from django import forms
from projectx_app.models.user import User
from projectx_app.models.user_detail import *
from django.conf import settings
from projectx_app.models.template import *


class TemplateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        self.fields['company'].required = False
        self.fields['template_doc'].required = True
        self.fields['template_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['template_type'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['template_status'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['template_doc'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['company'].widget.attrs['class'] = 'form-control r-0 light s-12'

    class Meta:
        model = Template
        fields = ('__all__')

    def save(self, request, commit=True):
        instance = super(TemplateForm, self).save(commit=False)
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

        if not self.instance.pk:
            # if create
            if commit:
                instance.company = company

        instance.save()

        return instance