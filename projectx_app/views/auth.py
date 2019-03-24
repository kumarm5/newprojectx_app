from django.shortcuts import render, redirect
from django.views import generic
from projectx_app.forms.auth import RegisterForm, LoginForm, ChangePasswordForm
from projectx_app.models.user import User, UserOTP
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
import boto3
import random


class Login(generic.TemplateView):
    template_name = 'projectx_app/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return self.render_to_response(
            self.get_context_data(
                form=form
            )
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if user.is_password_changed == False:
                        return redirect('change-password')
                    # if the user is applicant
                    if user.user_type == 1:
                        return redirect('dashboard')
                    # if the user is company admin
                    elif user.user_type == 2:
                        return redirect('company-user-dashboard')
                        # return redirect('company-account')
                    # if the user is company user
                    elif user.user_type == 6:
                        return redirect('company-user-dashboard')
                    # if the user is vendor admin
                    elif user.user_type == 3:
                        return redirect('vendor-admin-my-order')
                    # if the user is case worker
                    elif user.user_type == 4:
                        return redirect('vendor-user-my-cases')
                    # if user is rpo admin
                    elif user.user_type == 5:
                        return redirect('rpo-account')
                    elif user.user_type == 7:
                        return redirect('cmo-dashboard')
                    elif user.user_type == 8:
                        return redirect('hiring-manager-dashboard')
                    # if the user is rpo user
                    elif user.user_type == 9:
                        return redirect('company-user-dashboard')
                    elif user.is_superuser:
                        return redirect('company-listing')
                    return redirect('/dashboard')
            else:
                login_error = 1
                return self.render_to_response(
                    self.get_context_data(
                        login_error=login_error,
                        form=form,
                    )
                )
        else:
            login_error = 1
            return self.render_to_response(
                self.get_context_data(
                    login_error=login_error,
                    form=form,
                )
            )


class Register(generic.CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'projectx_app/register.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('change-password')
        # return redirect('dashboard')


def logout_view(request):
    logout(request)
    return redirect('login')


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password is successfully updated!')
            # return redirect('change-password')

            # if the user is applicant
            if request.user.user_type == 1:
                return redirect('dashboard')
            # if the user is company admin
            elif request.user.user_type == 2:
                return redirect('company-user-dashboard')
                # return redirect('company-account')
            # if the user is company user
            elif request.user.user_type == 6:
                return redirect('company-user-dashboard')
            # if the user is vendor admin
            elif request.user.user_type == 3:
                return redirect('vendor-admin-my-order')
            # if the user is case worker
            elif request.user.user_type == 4:
                return redirect('vendor-user-my-cases')
            # if user is rpo admin
            elif request.user.user_type == 5:
                return redirect('rpo-account')
            elif request.user.user_type == 7:
                return redirect('cmo-dashboard')
            elif request.user.user_type == 8:
                return redirect('hiring-manager-dashboard')
            # if the user is rpo user
            elif request.user.user_type == 9:
                return redirect('company-user-dashboard')
            elif user.is_superuser:
                return redirect('company-listing')
            return redirect('/dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'projectx_app/change_password.html', {
        'form': form
    })


def validate_email(request, email=None):
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this email already exists.'
    return JsonResponse(data)


def send_otp(request, mobile_number=None):
    client = boto3.client(
        "sns",
        aws_access_key_id="AKIAJRZJMZPTDHR4EN5A",
        aws_secret_access_key="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",
        region_name="ap-southeast-1"
    )

    otp_number = random.randint(1000,9999)

    is_sent = client.publish(
        PhoneNumber=mobile_number,
        Message="Your OTP number is {}".format(otp_number)
    )
    if is_sent:
        UserOTP.objects.create(mobile_number = mobile_number[2:], otp_number = otp_number)

    data = {
        'status': 'true'
    }

    return JsonResponse(data)
