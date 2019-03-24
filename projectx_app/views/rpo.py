from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.forms.rpo import *
from projectx_app.models.rpo import *
from projectx_app.models.company import *
from projectx_app.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse


class RpoAccountView(LoginRequiredMixin, CompanyGeneric, generic.UpdateView):
    model = SysRpo
    form_class = SysRpoForm
    template_name = 'projectx_app/rpo-account-info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            rpo_user = RPOUser.objects.get(user = self.request.user)
        except:
            rpo_user = None

        try:
            sysrpo = SysRpo.objects.get(id = rpo_user.rpo.id)
        except:
            sysrpo = None

        system_company_rpo = SystemCompanySetup.objects.filter(rpo_id = sysrpo.id, rpo_provider = True)

        context['system_company_rpo'] = system_company_rpo

        context['rpo_users'] = RPOUser.objects.filter(rpo = sysrpo)

        return context

    # get the object
    def get_object(self, *args, **kwargs):
        try:
            sysrpo = get_object_or_404(SysRpo, user=self.request.user)
        except:
            sysrpo = None
        return sysrpo

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'RPO Account information updated successfully')
        return redirect('rpo-account')


def rpo_company(request, company_id=None):
    sys_company = None

    if company_id:
        try:
            sys_company = SystemCompanySetup.objects.get(id = company_id)
        except:
            sys_company = None    

    if sys_company:
        request.session['company_id'] = sys_company.id
        data = {
            'status': 'true'
        }
    else:
        del request.session['company_id']
        data = {
            'status': 'false'
        }

    return JsonResponse(data)


class SysRPOView(LoginRequiredMixin, generic.ListView):
    model = SysRpo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        rpo = self.model.objects.filter(user__is_active = True)
        return rpo


class RPOInfoCreateView(LoginRequiredMixin, generic.CreateView):
    model = SysRpo
    form_class = SysRpoForm
    template_name = 'projectx_app/rpo-info-form.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        rpo = form.save(self.request)
        return redirect('sysrpo-listing')


class RPOInfoUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = SysRpo
    form_class = SysRpoForm
    template_name = 'projectx_app/rpo-info-form.html'
    success_url = reverse_lazy('sysrpo-listing')

    # get the object
    def get_object(self, *args, **kwargs):
        rpoinfo = get_object_or_404(SysRpo, pk=self.kwargs['id'])
        return rpoinfo

    def form_valid(self, form):
        rpo = form.save(self.request)
        return redirect('sysrpo-listing')


def delete_rpo_info(request, rpo_id=None):
    '''
        This function is used to delete the rpo.
    '''
    try:
        delete_rpo = User.objects.filter(pk = int(rpo_id)).update(is_active = False)
    except:
        delete_rpo = None

    if delete_rpo:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }

    return JsonResponse(data)


class RPOUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = RPOUser
    form_class = RPOUserForm
    template_name = 'projectx_app/rpo-user-form.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        instance = form.save(self.request)
        return redirect('rpo-account')


class RPOUserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = RPOUser
    form_class = RPOUserForm
    template_name = 'projectx_app/rpo-user-form.html'
    success_url = reverse_lazy('rpo-account')

    # get the object
    def get_object(self, *args, **kwargs):
        rpouser = get_object_or_404(RPOUser, pk=self.kwargs['rpo_id'])
        return rpouser

    def form_valid(self, form):
        rpouser = form.save(self.request)
        return redirect('rpo-account')
