from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.forms.template import *
from projectx_app.models.template import *
from projectx_app.models.company import *
from projectx_app.views.generic import *
from projectx_app.models.user_detail import *
from projectx_app.forms.rpo import *
from projectx_app.models.rpo import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse


class CompanyTemplateView(LoginRequiredMixin, CompanyGeneric, generic.ListView):
    model = Template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        company = None
        if 'company_id' in self.request.session:
            try:
                company = SystemCompanySetup.objects.get(pk = self.request.session['company_id'])
            except:
                company = None
        else:
            try:
                companyuser = CompanyUser.objects.get(user = self.request.user)
            except:
                companyuser = None

            if companyuser:
                company = companyuser.company

        templates = self.model.objects.filter(is_delete = False, company = company)
        return templates

class RpoCompanyTemplateView(LoginRequiredMixin, generic.ListView):
    model = Template
    company = []
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        company = None
        getDetails = SysRpo.objects.get(user_id=self.request.user)
        getUsers = SystemCompanySetup.objects.filter(rpo=getDetails)
        company = []
        for CUsers in getUsers:
            try:
                companyuser = CompanyUser.objects.get(company=CUsers)
            except:
                companyuser = None

            if companyuser:
                company.append(companyuser.company)

        templates = self.model.objects.filter(is_delete = False, company__in= company)
        return templates


class TemplateCreateView(LoginRequiredMixin, CompanyGeneric, generic.CreateView):
    model = Template
    form_class = TemplateForm
    template_name = 'projectx_app/template-form.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        template = form.save(self.request)
        return redirect('template-listing')


class TemplateUpdateView(LoginRequiredMixin, CompanyGeneric, generic.UpdateView):
    model = Template
    form_class = TemplateForm
    template_name = 'projectx_app/template-form.html'
    success_url = reverse_lazy('template-listing')

    # get the object
    def get_object(self, *args, **kwargs):
        template = get_object_or_404(Template, pk=self.kwargs['id'])
        return template

    def form_valid(self, form):
        template = form.save(self.request)
        return redirect('template-listing')


def delete_template_info(request, template_id=None):
    '''
        This function is used to delete template.
    '''
    try:
        delete_template = Template.objects.filter(pk = int(template_id)).update(is_delete = False)
    except:
        delete_template = None

    if delete_template:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }

    return JsonResponse(data)
