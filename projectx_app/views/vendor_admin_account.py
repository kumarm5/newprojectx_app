from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.models.onboarding import *
from projectx_app.models.request import *
from projectx_app.models.vendor import *
from projectx_app.forms.vendor import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse


class VendorAdminMyAccountView(LoginRequiredMixin, generic.UpdateView):
    model = VendorMaster
    form_class = VendorMasterForm
    template_name = 'projectx_app/vendor-my-account.html'
    success_url = reverse_lazy('vendor-admin-account-detail')

    def get_context_data(self, **kwargs):
        try:
            vendoruser = CompanyVendor.objects.filter(user = self.request.user).last()
        except:
            vendoruser = None

        kwargs['vendor_users'] = CompanyVendor.objects.filter(vendor = vendoruser.vendor, user__user_type = 4)
        return super().get_context_data(**kwargs)

    # get the object
    def get_object(self, *args, **kwargs):
        try:
            vendoruser = CompanyVendor.objects.filter(user = self.request.user).last()
        except:
            vendoruser = None

        my_request = get_object_or_404(VendorMaster, pk = vendoruser.vendor.id)
        return my_request

    def form_valid(self, form):
        user = form.save(self.request)
        messages.success(self.request, 'Your Accout Information is successfully updated!')
        return redirect('vendor-admin-account-detail')


class VendorAccountUserCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = VendorUserForm
    template_name = 'projectx_app/vendor-user-form.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(self.request)
        return redirect('vendor-admin-account-detail')


class VendorAccountUserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CompanyVendor
    form_class = VendorUserForm
    template_name = 'projectx_app/vendor-user-form.html'
    success_url = reverse_lazy('vendor-admin-account-detail')

    # get the object
    def get_object(self, *args, **kwargs):
        vendorusers = get_object_or_404(CompanyVendor, pk=self.kwargs['id'])
        return vendorusers

    def form_valid(self, form):
        user = form.save(self.request)
        return redirect('vendor-admin-account-detail')