from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.models.task import *
from projectx_app.models.request import *
from projectx_app.models.user import *
from projectx_app.models.company import *


class ApplicantGeneric(generic.View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            personal_info = PersonalInfo.objects.get(user = self.request.user)
        except:
            personal_info = None

        # get the total task from the request task table for the applicant
        my_requested_tasks = MyRequestTasksInfo.objects.filter(myrequest__applicant__user = self.request.user)

        my_requested_tasks_count = my_requested_tasks.count()

        for my_request in my_requested_tasks:
            try:
                mark_complete = MyRequestTasks.objects.get(myrequest = my_request.myrequest, step_id = my_request.step_id, mark_complete = True)
            except:
                mark_complete = None

            if mark_complete:
                my_requested_tasks_count = my_requested_tasks_count - 1

        context['open_task'] = my_requested_tasks_count
        context['personal_info'] = personal_info

        if personal_info:
            context['profile_pic'] = personal_info.profile_pic.name

        return context


class CompanyGeneric(generic.View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_setup = None

        if 'company_id' in self.request.session:
            try:
                company = SystemCompanySetup.objects.get(pk = self.request.session['company_id'])
            except:
                company = None

            if company:
                try:
                    context['company_logo'] = company.logo_image.url
                except:
                    context['company_logo'] = None
                try:
                    context['company_name'] = company.company_name
                except:
                    context['company_name'] = None
        else:
            try:
                company_user = CompanyUser.objects.get(user = self.request.user)
            except:
                company_user = None

            if company_user:
                company_setup = SystemCompanySetup.objects.get(pk = company_user.company.id)

            if company_setup:
                try:
                    context['company_logo'] = company_setup.logo_image.url
                except:
                    context['company_logo'] = None
                try:
                    context['company_name'] = company_setup.company_name
                except:
                    context['company_name'] = None                
        return context
