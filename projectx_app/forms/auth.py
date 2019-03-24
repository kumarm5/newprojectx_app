from django import forms
from projectx_app.models.user import User, UserOTP
from projectx_app.models.user_detail import *
from projectx_app.models.applicant import *
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.mail import EmailMessage
from django.db import transaction
from django.conf import settings


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control r-0 light s-12'

    def save(self):
        instance = super().save(commit=False)
        instance.is_password_changed = True
        instance.save()
        return instance


class RegisterForm(UserCreationForm):
    # otp = forms.CharField(max_length=5)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control form-control-lg no-b'        
        self.fields['password1'].widget.attrs['onKeyUp'] = 'checkPasswordStrength();'

        self.fields['password2'].widget.attrs['class'] = 'form-control form-control-lg no-b'
        # self.fields['otp'].widget.attrs['class'] = 'form-control form-control-lg no-b'
        # self.fields['otp'].widget.attrs['placeholder'] = 'Enter OTP'        
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1','password2', 'mobile_number')

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg no-b',
                    'placeholder': 'First Name',
                    'autocomplete': 'off'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg no-b',
                    'placeholder': 'Last Name',
                    'autocomplete': 'off'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control form-control-lg no-b',
                    'placeholder': 'Email Address',
                    'autocomplete': 'off'
                }
            ),
            'mobile_number': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg no-b',
                    'placeholder': 'Mobile Number',
                    'autocomplete': 'off'
                }
            )
        }

    # def clean(self):
    #     cleaned_data = super(RegisterForm, self).clean()
    #     otp = cleaned_data.get("otp")
    #     mobile_number = cleaned_data.get("mobile_number")
        
    #     try:
    #         user_otp = UserOTP.objects.filter(otp_number = otp, mobile_number = mobile_number).last()
    #     except:
    #         user_otp = None

    #     if user_otp == None:
    #         raise forms.ValidationError("Enter valid OTP.")

    #     return cleaned_data


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = 1 # 1 = applicant
        user.save()
        applicant = Applicant.objects.create(user=user)

        html_message = "Dear Applicant,"+"<br><br>Welcome to Plat X. We are delighted to have you onboard !<br><br><br><br>If you have any questions we are here to help – please drop in an email to support@xyz.com<br><br>Cheers,<br>Team XYZ<br>"
        email_message = EmailMessage('Welcome to Plat X', html_message, settings.EMAIL_HOST_USER, [],[user.email])
        email_message.content_subtype = "html"
        email_message.send()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control form-control-lg no-b r-0 light s-12'
        self.fields['password'].widget.attrs['class'] = 'form-control form-control-lg no-b r-0 light s-12'

        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
