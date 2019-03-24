from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.forms.vendor import *
from projectx_app.models.vendor import *
from projectx_app.models.master import *
from projectx_app.models.task import *
from projectx_app.models.user import *
from projectx_app.forms.rpo import *
from projectx_app.views.generic import *
from projectx_app.models.rpo import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

class MyVendorListView(LoginRequiredMixin, CompanyGeneric, generic.ListView):
    model = CompanyVendor
    def get_context_data(self, *args, **kwargs):
        context = super(MyVendorListView, self).get_context_data(*args, **kwargs)
        company = None

        if 'company_id' in self.request.session:
            context['co_vendor'] = CompanyVendor.objects.filter(company_id = self.request.session['company_id'], user__user_type = 3) #vendor admin
        else:
            try:
                companyuser = CompanyUser.objects.get(user = self.request.user)
            except:
                companyuser = None

            if companyuser:
                company = companyuser.company


            context['co_vendor'] = CompanyVendor.objects.filter(company = company, user__user_type = 3) #vendor admin
        return context

    def get_queryset(self):
        #super admin vendor listing
        company_vendor = self.model.objects.filter(user__user_type = 3) #vendor admin
        return company_vendor


class MyRpoVendorListView(LoginRequiredMixin, generic.ListView):
    model = CompanyVendor
    def get_context_data(self, *args, **kwargs):
        context = super(MyRpoVendorListView, self).get_context_data(*args, **kwargs)
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

        context['co_vendor'] = CompanyVendor.objects.filter(company__in=company)
        return context

    def get_queryset(self):
        vendor_master = self.model.objects.all()
        return vendor_master

class MyVendorCreateView(LoginRequiredMixin, CompanyGeneric, generic.TemplateView):
    template_name = 'projectx_app/vendor-form.html'
    form_class = VendorMasterForm
    def get(self, request, *args, **kwargs):
        form = VendorMasterForm()
        co_vendor_form = CompanyVendorForm()

        return self.render_to_response(
            self.get_context_data(
                form=form,
                co_vendor_form = co_vendor_form,
            )
        )

    def post(self, request, *args, **kwargs):
        form = VendorMasterForm(request.POST)
        co_vendor_form = CompanyVendorForm(request.POST, request.FILES)

        # service_provider_type = request.POST['service_provider_type']

        if form.is_valid() and co_vendor_form.is_valid():            
            vendor_master_instance = form.save(self.request)

            if vendor_master_instance:
                co_vendor_form.save(vendor_master_instance, request)

            return redirect('vendor-user-listing')
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    co_vendor_form = co_vendor_form,
                )
            )

class MyVendorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CompanyVendor
    form_class = VendorForm
    template_name = 'projectx_app/company-vendor-form.html'
    success_url = reverse_lazy('vendor-user-listing')

    # get the object
    def get_object(self, *args, **kwargs):
        vendor_info = get_object_or_404(CompanyVendor, pk=self.kwargs['id'])
        return vendor_info



class AddCompanyVendor(LoginRequiredMixin, generic.TemplateView):
    template_name = 'projectx_app/vendor-form.html'
    form_class = AddVendorMasterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'company_id' in self.request.session:
            try:
                context['company'] = SystemCompanySetup.objects.get(pk = self.request.session['company_id'])
            except:
                context['company'] = None
        else:
            try:
                company_user = CompanyUser.objects.get(user = self.request.user)
            except:
                company_user = None

            context['company'] = company_user.company
        return context

    def get(self, request, *args, **kwargs):
        try:
            vendor_master = VendorMaster.objects.get(id = self.kwargs['id'])
        except:
            vendor_master = VendorMaster()

        form = AddVendorMasterForm(instance = vendor_master)
        co_vendor_form = AddCompanyVendorForm()

        return self.render_to_response(
            self.get_context_data(
                form=form,
                co_vendor_form = co_vendor_form,
            )
        )

    def post(self, request, *args, **kwargs):
        try:
            vendor_master = VendorMaster.objects.get(pk = int(request.POST['vendor']))
        except:
            vendor_master = None

        try:
            user = User.objects.get(email = vendor_master.email)
        except:
            user = None

        form = AddVendorMasterForm(request.POST)
        co_vendor_form = AddCompanyVendorForm(request.POST, request.FILES)
        if co_vendor_form.is_valid():
            co_vendor_form.save(request, user)
            return redirect('vendor-user-listing')
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    co_vendor_form = co_vendor_form,
                )
            )


def search_vendor(request):
    data_array = []
    vendors = None
    search_content = request.POST['search_content']

    #if rpo user company is set in the session
    if 'company_id' in request.session:
        vendors = CompanyVendor.objects.filter(
            company_id = request.session['company_id'],
            vendor__vendor_company_name__icontains = search_content,
            user__user_type = 3, # vendor admin
            ).values_list('vendor_id', flat=True)
    else:
    # if company user is logged in
        try:
            companyuser = CompanyUser.objects.get(user = request.user)
        except:
            companyuser = None

        if companyuser:
            vendors = CompanyVendor.objects.filter(
                company = companyuser.company,
                vendor__vendor_company_name__icontains = search_content,
                user__user_type = 3, # vendor admin
                ).values_list('vendor_id', flat=True)

    vendor_masters = VendorMaster.objects.filter(
        vendor_company_name__icontains = search_content,
    ).exclude(id__in = list(vendors))

    if vendor_masters:
        for vendor in vendor_masters:
            data_array.append({
                'vendor_id': vendor.id,
                'vendor': vendor.vendor_company_name,
                'email': vendor.email,
                'date_time': vendor.created_at,
            })

    return JsonResponse(data_array, safe=False)


class CompanyVendorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CompanyVendor
    form_class = VendorForm
    template_name = 'projectx_app/company-vendor-form.html'
    success_url = reverse_lazy('vendor-user-listing')

    # get the object
    def get_object(self, *args, **kwargs):
        vendor_info = get_object_or_404(CompanyVendor, pk=self.kwargs['id'])
        return vendor_info


def vendor_email(request, id=None):
    try:
        company_vendor = CompanyVendor.objects.get(pk = id)
    except:
        company_vendor = None

    if company_vendor:
        status = {
            "vendor-email": company_vendor.user.email
        }
    else:
        status = {
            "vendor-email": ""
        }

    return JsonResponse(status)
