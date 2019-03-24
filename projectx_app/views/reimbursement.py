from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.models.reimbursement import *
from projectx_app.forms.reimbursement import *
from projectx_app.views.generic import ApplicantGeneric

class ReimbursementListView(LoginRequiredMixin, ApplicantGeneric, generic.ListView):
    model = Reimbursement
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ReimbursementCreateView(LoginRequiredMixin, ApplicantGeneric, generic.CreateView):
    model = Reimbursement
    form_class = ReimbursementForm
    template_name = 'projectx_app/reimbursement-form.html'

    def form_valid(self, form):
        reimbursement = form.save(self.request)
        return redirect('my-reimbursement')

    def get_form_kwargs(self):
        kwargs = super(ReimbursementCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ReimbursementUpdateView(LoginRequiredMixin, ApplicantGeneric, generic.UpdateView):
    model = Reimbursement
    form_class = ReimbursementForm
    template_name = 'projectx_app/reimbursement-form.html'
    success_url = reverse_lazy('my-reimbursement')

    # get the object
    def get_object(self, *args, **kwargs):
        reimbursement = get_object_or_404(Reimbursement, pk=self.kwargs['reimbursement_id'])
        return reimbursement

    def form_valid(self, form):
        reimbursement = form.save(self.request)
        return redirect('my-reimbursement')

    def get_form_kwargs(self):
        kwargs = super(ReimbursementUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs