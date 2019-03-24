from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.forms.user_detail import *
from projectx_app.models.user_detail import *
from projectx_app.models.applicant import *
from projectx_app.forms.applicant import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse


class ApplicantUserView(LoginRequiredMixin, generic.ListView):
    model = Applicant
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        applicant_user = self.model.objects.filter(user__is_active = True)
        return applicant_user


class ApplicantUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Applicant
    form_class = ApplicantForm
    template_name = 'projectx_app/applicant-form.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        companyuser = form.save()
        return redirect('applicant-listing')


class ApplicantUserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Applicant
    form_class = ApplicantForm
    template_name = 'projectx_app/applicant-form.html'
    success_url = reverse_lazy('applicant-listing')

    # get the object
    def get_object(self, *args, **kwargs):
        applicantuser = get_object_or_404(Applicant, pk=self.kwargs['id'])
        return applicantuser


def delete_applicant_info(request, applicant_id=None):
    '''
        This function is used to delete applicant user.
    '''
    try:
        delete_applicant = User.objects.filter(pk = int(applicant_id)).update(is_active = False)
    except:
        delete_applicant = None

    if delete_applicant:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }

    return JsonResponse(data)

