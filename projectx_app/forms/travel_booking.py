from django import forms
from projectx_app.models.user import User
from projectx_app.models.user_detail import *
from projectx_app.models.travel_booking import *
from projectx_app.models.vendor import *
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage


class TravelBookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user =  kwargs.pop('user')
        super(TravelBookingForm, self).__init__(*args, **kwargs)
        self.fields['myrequest'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['vendor'].widget.attrs['class'] = 'form-control r-0 light s-12'

        try:
            company_user = CompanyUser.objects.get(user = user)
        except:
            company_user = None

        if company_user:
            self.fields['vendor'].queryset = CompanyVendor.objects.filter(
                sys_vendor_type__type_description__icontains = 'Travel',
                company = company_user.company
            )
        else:
            self.fields['vendor'].queryset = CompanyVendor.objects.filter(
                sys_vendor_type__type_description__icontains = 'Travel'
            )

        self.fields['vendor_email'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['due_date'].widget.attrs['class'] = 'form-control r-0 light s-12 date-picker'
        self.fields['attached_template'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['comments'].widget.attrs['class'] = 'form-control r-0 light s-12'        
        self.fields['due_date'].widget.attrs['autocomplete'] = "off"

    class Meta:
        model = TravelBooking
        fields = ('__all__')

    def save(self, commit=True):
        instance = super(TravelBookingForm, self).save(commit=True)

        vendor_email = self.cleaned_data.get('vendor_email')

        try:
            user = User.objects.get(email = vendor_email)
        except:
            user = None

        if instance.attached_template:
            fs = FileSystemStorage()
            fs.location = fs.location+'/media/'
            filename = fs.save(instance.attached_template.name, instance.attached_template)

        if user:
            html_message = "Dear "+user.first_name+", <br><br>Please have a look at attached files for travel details. <br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
            email_message = EmailMessage('Travel Booked', html_message, settings.EMAIL_HOST_USER, [],[user.email])
            email_message.content_subtype = "html"

            if instance.attached_template:
                filename = 'media/'+filename
                email_message.attach_file(filename)
            email_message.send()
