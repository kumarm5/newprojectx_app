from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.forms.user_detail import *
from projectx_app.models.user_detail import *
from projectx_app.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.core.files.storage import FileSystemStorage


class Dashboard(LoginRequiredMixin, ApplicantGeneric, generic.TemplateView):
    template_name = 'projectx_app/dashboard.html'
    form_class = PersonalInfoForm
    def get(self, request, *args, **kwargs):
        form = UserForm(instance = request.user)
        personalinfo_form = self.form_class(instance = request.user.user_personal_info)
        return self.render_to_response(
            self.get_context_data(
                form=form,
                personalinfo_form = personalinfo_form,
            )
        )

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, instance = request.user)
        personalinfo_form = self.form_class(request.POST, request.FILES, instance = request.user.user_personal_info)

        if form.is_valid() and personalinfo_form.is_valid():
            form.save()
            personalinfo_form.save(request)
            messages.success(request, 'Personal information updated successfully')
            return redirect('/dashboard')
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    personalinfo_form = personalinfo_form,
                )
            )


class ContactViewInfo(LoginRequiredMixin, ApplicantGeneric, generic.TemplateView):
    template_name = 'projectx_app/contact-info.html'
    form_class = ContactInfoForm

    def get(self, request, *args, **kwargs):
        try:
            contact_instance = ContactInfo.objects.get(user=request.user)
            address_instance = AddressInfo.objects.get(user=request.user)
            form = self.form_class(instance=contact_instance)
            address_form = AddressInfoForm(instance=address_instance)
        except Exception as e:
            form = self.form_class
            address_form = AddressInfoForm

        return self.render_to_response(
            self.get_context_data(
                form=form,
                address_form = address_form,
            )
        )

    def post(self, request, *args, **kwargs):
        try:
            contact_instance = ContactInfo.objects.get(user=request.user)
        except:
            contact_instance = None

        try:
            address_instance = AddressInfo.objects.get(user=request.user)
        except:
            address_instance = None

        form = self.form_class(request.POST, instance = contact_instance)
        address_form = AddressInfoForm(request.POST, instance = address_instance)

        if form.is_valid() and address_form.is_valid():
            form_obj = form.save(commit=False)
            address_form_obj = address_form.save(commit=False)
            form_obj.user = request.user
            address_form_obj.user = request.user
            form_obj.save()
            address_form_obj.save()

            messages.success(request, 'Contact information updated successfully')
            return redirect('contact-info')
        else:

            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    address_form=address_form,
                )
            )


class IDInfoView(LoginRequiredMixin, ApplicantGeneric, generic.ListView):
    model = GovernmentIssuedIDs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        user_identity = self.model.objects.filter(user=self.request.user, is_deleted = False)
        return user_identity


class IDInfoCreateView(LoginRequiredMixin, ApplicantGeneric, generic.CreateView):
    model = GovernmentIssuedIDs
    form_class = GovernmentIssuedIDsForm
    template_name = 'projectx_app/idinfo-form.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        id_listing = form.save()
        return redirect('id-info-listing')


class IDInfoUpdateView(LoginRequiredMixin, ApplicantGeneric, generic.UpdateView):
    model = GovernmentIssuedIDs
    form_class = GovernmentIssuedIDsForm
    template_name = 'projectx_app/idinfo-form.html'
    success_url = reverse_lazy('id-info-listing')

    # get the object
    def get_object(self, *args, **kwargs):
        idinfo = get_object_or_404(GovernmentIssuedIDs, pk=self.kwargs['id'])
        return idinfo


def delete_identification_info(request, gov_id):
    '''
        This function is used to delete the identification information.
    '''
    try:
        delete_identification = GovernmentIssuedIDs.objects.filter(pk = int(gov_id)).update(is_deleted = True)
    except:
        delete_identification = None

    if delete_identification:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }

    return JsonResponse(data)



class WorkInfoView(LoginRequiredMixin, ApplicantGeneric, generic.ListView):
    model = WorkInfo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        user_work = self.model.objects.filter(user=self.request.user, is_deleted = False)
        return user_work



class WorkInfoCreateView(LoginRequiredMixin, ApplicantGeneric, generic.CreateView):
    model = WorkInfo
    form_class = WorkInfoForm
    template_name = 'projectx_app/work-info-form.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        work_listing = form.save()
        return redirect('work-info-listing')


class WorkInfoUpdateView(LoginRequiredMixin, ApplicantGeneric, generic.UpdateView):
    model = WorkInfo
    form_class = WorkInfoForm
    template_name = 'projectx_app/work-info-form.html'
    success_url = reverse_lazy('work-info-listing')

    # get the object
    def get_object(self, *args, **kwargs):
        workinfo = get_object_or_404(WorkInfo, pk=self.kwargs['id'])
        return workinfo


def delete_work_info(request, work_id):
    '''
        This function is used to delete the work information.
    '''
    try:
        delete_work = WorkInfo.objects.filter(pk = int(work_id)).update(is_deleted = True)
    except:
        delete_work = None

    if delete_work:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }

    return JsonResponse(data)


class EducationInfoView(LoginRequiredMixin, ApplicantGeneric, generic.ListView):
    model = EducationInfo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        user_education = self.model.objects.filter(user=self.request.user, is_deleted = False)
        return user_education


class EducationInfoCreateView(LoginRequiredMixin, ApplicantGeneric, generic.CreateView):
    model = EducationInfo
    form_class = EducationInfoForm
    template_name = 'projectx_app/education-info-form.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        work_listing = form.save()
        return redirect('education-info-listing')


class EducationInfoUpdateView(LoginRequiredMixin, ApplicantGeneric, generic.UpdateView):
    model = EducationInfo
    form_class = EducationInfoForm
    template_name = 'projectx_app/education-info-form.html'
    success_url = reverse_lazy('education-info-listing')

    # get the object
    def get_object(self, *args, **kwargs):
        educationinfo = get_object_or_404(EducationInfo, pk=self.kwargs['id'])
        return educationinfo


def delete_education_info(request, education_id):
    '''
        This function is used to delete the education information.
    '''
    try:
        delete_education = EducationInfo.objects.filter(pk = int(education_id)).update(is_deleted = True)
    except:
        delete_education = None

    if delete_education:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }

    return JsonResponse(data)

