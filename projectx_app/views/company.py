from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.models.task import *
from projectx_app.models.user import *
from projectx_app.forms.company import *
from projectx_app.forms.request import MyRequestTasksInfoForm
from projectx_app.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q


class CompanyAccountView(LoginRequiredMixin, CompanyGeneric, generic.UpdateView):
    model = SystemCompanySetup
    form_class = CompanySetUpForm
    template_name = 'projectx_app/company-account.html'

    # get the object
    def get_object(self, *args, **kwargs):
        try:
            companyuser = CompanyUser.objects.get(user = self.request.user)
        except:
            companyuser = None

        companysetup = get_object_or_404(SystemCompanySetup, pk=companyuser.company.id)
        return companysetup

    def form_valid(self, form):
        companysetup = form.save(self.request)
        messages.success(self.request, 'Company Account information updated successfully')
        return redirect('company-account')


class SystemCompanySetupView(LoginRequiredMixin, generic.ListView):
    model = SystemCompanySetup
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        company_user = self.model.objects.all()
        return company_user



class SystemCompanySetupCreateView(LoginRequiredMixin, generic.CreateView):
    model = SystemCompanySetup
    form_class = CompanySetUpForm
    template_name = 'projectx_app/systemcompanysetup-form.html'

    def get_context_data(self, **kwargs):        
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        companyuser = form.save(self.request)
        return redirect('company-listing')


class SystemCompanySetupUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = SystemCompanySetup
    form_class = CompanySetUpForm
    template_name = 'projectx_app/systemcompanysetup-form.html'
    success_url = reverse_lazy('company-listing')

    # get the object
    def get_object(self, *args, **kwargs):
        companysetup = get_object_or_404(SystemCompanySetup, pk=self.kwargs['id'])
        return companysetup

    def form_valid(self, form):
        companysetup = form.save(self.request)
        return redirect('company-listing')


def delete_systemcompanysetup_info(request, systemcompanysetup_id=None):
    '''
        This function is used to delete system company user.
    '''
    try:
        delete_sys_company = User.objects.filter(pk = int(systemcompanysetup_id)).update(is_active = False)
    except:
        delete_sys_company = None

    if delete_sys_company:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }

    return JsonResponse(data)



class CompanyUserView(LoginRequiredMixin, CompanyGeneric, generic.ListView):
    model = CompanyUser
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
                companyuser = self.model.objects.get(user = self.request.user)
            except:
                companyuser = None

            if companyuser:
                company = companyuser.company

        company_user = self.model.objects.filter(company = company)
        return company_user


class CompanyUserCreateView(LoginRequiredMixin, CompanyGeneric, generic.CreateView):
    model = CompanyUser
    form_class = CompanyUserForm
    template_name = 'projectx_app/companyuser-form.html'

    def get_context_data(self, **kwargs):        
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        companyuser = form.save(self.request)
        return redirect('company-user-listing')


class CompanyUserUpdateView(LoginRequiredMixin, CompanyGeneric, generic.UpdateView):
    model = CompanyUser
    form_class = CompanyUserForm
    template_name = 'projectx_app/companyuser-form.html'
    success_url = reverse_lazy('company-listing')

    # get the object
    def get_object(self, *args, **kwargs):
        companyuser = get_object_or_404(CompanyUser, pk=self.kwargs['id'])
        return companyuser

    def form_valid(self, form):
        companyuser = form.save(self.request)
        return redirect('company-user-listing')


def delete_company_user_info(request, company_user_id=None):
    '''
        This function is used to delete company user.
    '''
    try:
        delete_company_user = User.objects.filter(pk = int(company_user_id)).update(is_active = False)
    except:
        delete_company_user = None

    if delete_company_user:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }

    return JsonResponse(data)


class CompanyUserDashboard(LoginRequiredMixin, CompanyGeneric, generic.ListView):
    template_name = 'projectx_app/companyuser-dashboard.html'
    model = MyRequest

    def get_context_data(self, *args, **kwargs):
        context = super(CompanyUserDashboard, self).get_context_data(*args, **kwargs)
        
        try:
            rpo_user = RPOUser.objects.get(user = self.request.user)
        except:
            rpo_user = None

        try:
            sysrpo = SysRpo.objects.get(id = rpo_user.rpo.id)
        except:
            sysrpo = None

        if rpo_user:
            system_company_rpo = SystemCompanySetup.objects.filter(rpo_id = sysrpo.id, rpo_provider = True)
        else:
            system_company_rpo = None

        context['system_company_rpo'] = system_company_rpo

        return context

    def get_queryset(self):
        my_request_tasks = None

        if 'company_id' in self.request.session:
            try:
                company = SystemCompanySetup.objects.get(pk = self.request.session['company_id'])
            except:
                company = None

            if self.request.user.user_type == 9: # rpo user
                my_request_tasks = self.model.objects.filter(created_by = self.request.user)
            else:
                my_request_tasks = self.model.objects.filter(company = company)
        else:
            try:
                companyuser = CompanyUser.objects.get(user = self.request.user)
            except:
                companyuser = None

            if companyuser:
                if companyuser.user.user_type == 2: # company admin
                    my_request_tasks = self.model.objects.filter(company = companyuser.company)
                elif companyuser.user.user_type == 6:# company user
                    my_request_tasks = self.model.objects.filter(created_by = self.request.user)

        return my_request_tasks


class CMOUserDashboard(LoginRequiredMixin, CompanyGeneric, generic.ListView):
    template_name = 'projectx_app/cmo-dashboard.html'
    model = MyRequestTasksInfo

    def get_context_data(self, *args, **kwargs):
        context = super(CMOUserDashboard, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        my_request_tasks = None

        if self.request.user.user_type == 7: # company cmo user
            try:
                company_user = CompanyUser.objects.get(user = self.request.user)
            except:
                company_user = None

            if company_user:
                my_request_tasks_one = MyRequestTasksInfo.objects.filter(
                    company =company_user.company,
                    step_id__in = ['4'], 
                    is_vendor_action = True,
                    progress_status__in = ['Completed', 'Assigned', 'In Progress'],
                    result__in = ['All Clear', 'Minor Issues', 'Serious medical condition']
                )

                my_request_tasks_two = MyRequestTasksInfo.objects.filter(
                    company =company_user.company,
                    step_id__in = ['4'],
                    send_to_candidate = True
                )

                my_request_tasks = my_request_tasks_one.union(my_request_tasks_two)

        return my_request_tasks


class CMOUserMyCaseForm(LoginRequiredMixin, generic.UpdateView):
    model = MyRequestTasksInfo
    form_class = MyRequestTasksInfoForm
    template_name = 'projectx_app/cmo-user-my-cases-form.html'
    success_url = reverse_lazy('cmo-dashboard')

    # get the object
    def get_object(self, *args, **kwargs):
        request_task_info = get_object_or_404(MyRequestTasksInfo, pk=self.kwargs['id'])
        return request_task_info

    def form_valid(self, form):
        instance = form.save(self.request)
        if instance:
            messages.success(self.request, 'Task information is updated successfully.')
        return redirect('cmo-dashboard')

    def get_form_kwargs(self):
        kwargs = super(CMOUserMyCaseForm, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class HiringManagerDashboard(LoginRequiredMixin, CompanyGeneric, generic.ListView):
    template_name = 'projectx_app/hiring-manager-dashboard.html'
    model = MyRequestTasksInfo

    def get_context_data(self, *args, **kwargs):
        context = super(HiringManagerDashboard, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        my_request_tasks = None

        if self.request.user.user_type == 8: # hiring manager user
            try:
                company_user = CompanyUser.objects.get(user = self.request.user)
            except:
                company_user = None

            if company_user:
                my_request_tasks = MyRequestTasksInfo.objects.filter(
                    myrequest__hiring_manager_user = company_user, 
                    step_id__in = ['1','2'], 
                    is_vendor_action = True,
                    progress_status__in = ['Completed'],
                    result__in = ['Request can not be processed', 'Failed']
                    )

                # my_request_tasks_two = MyRequestTasksInfo.objects.filter(
                #     myrequest__hiring_manager_user = company_user, 
                #     step_id__in = ['4'], 
                #     is_vendor_action = True,
                #     is_cmo_action = True,
                #     progress_status__in = ['Completed'],
                #     result__in = ['Request can not be processed', 'Failed']
                #     )

                # my_request_tasks = my_request_tasks_one.union(my_request_tasks_two)

        return my_request_tasks


class HiringManagerUserMyCaseForm(LoginRequiredMixin, generic.UpdateView):
    model = MyRequestTasksInfo
    form_class = MyRequestTasksInfoForm
    template_name = 'projectx_app/hiring-manager-user-my-cases-form.html'
    success_url = reverse_lazy('hiring-manager-dashboard')

    # get the object
    def get_object(self, *args, **kwargs):
        request_task_info = get_object_or_404(MyRequestTasksInfo, pk=self.kwargs['id'])
        return request_task_info

    def form_valid(self, form):
        instance = form.save(self.request)
        if instance:
            messages.success(self.request, 'Task information is updated successfully.')
        return redirect('hiring-manager-dashboard')

    def get_form_kwargs(self):
        kwargs = super(HiringManagerUserMyCaseForm, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
