from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.models.medical_check import *
from projectx_app.forms.medical_check import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse


class MedicalCheckCreateView(LoginRequiredMixin, generic.CreateView):
    model = MedicalCheck
    form_class = MedicalCheckUpForm
    template_name = 'projectx_app/medical-check-form.html'

    def get_form_kwargs(self):
        kwargs = super(MedicalCheckCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        try:
            my_request = MyRequest.objects.get(pk = int(self.kwargs['request_id']))
        except:
            my_request = None

        context['my_request'] = my_request
        return context

    def form_valid(self, form):
        work_listing = form.save()
        messages.success(self.request, 'Medical Check information is updated successfully.')
        return redirect('company-user-dashboard')
