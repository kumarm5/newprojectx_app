from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from projectx_app.models.user import User
from projectx_app.models.task import *
from projectx_app.models.request import *
from projectx_app.models.vendor import *
from projectx_app.forms.request import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy


class VendorUserMyCase(LoginRequiredMixin, generic.ListView):
    template_name = 'projectx_app/vendor-user-my-cases.html'
    model = MyRequestTasksInfo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            vendor_user = CompanyVendor.objects.get(user = self.request.user)
        except:
            vendor_user = None

        if vendor_user:
            context['vendors'] = CompanyVendor.objects.filter(vendor = vendor_user.vendor)
        else:
            context['vendors'] = None
        return context

    def get_queryset(self):
        my_request_task_info = self.model.objects.filter(vendor_user__user_id = self.request.user.id)
        return my_request_task_info


class VendorUserMyCaseForm(LoginRequiredMixin, generic.UpdateView):
    model = MyRequestTasksInfo
    form_class = MyRequestTasksInfoForm
    template_name = 'projectx_app/vendor-user-my-cases-form.html'
    success_url = reverse_lazy('vendor-user-my-cases')

    # get the object
    def get_object(self, *args, **kwargs):
        request_task_info = get_object_or_404(MyRequestTasksInfo, pk=self.kwargs['id'])
        return request_task_info

    def form_valid(self, form):
        instance = form.save(self.request)
        if instance:
            messages.success(self.request, 'Task information is updated successfully.')
        return redirect('vendor-user-my-cases')

    def get_form_kwargs(self):
        kwargs = super(VendorUserMyCaseForm, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs