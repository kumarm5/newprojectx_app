from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from projectx_app.forms.document import *
from projectx_app.models.document import *
from projectx_app.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.forms import inlineformset_factory


class DocumentInfoView(LoginRequiredMixin, ApplicantGeneric, generic.ListView):
    model = Document
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = DocumentFiles.objects.all()
        return context

    def get_queryset(self):
        user_documents = self.model.objects.filter(user=self.request.user, is_deleted = False)
        return user_documents


class DocumentInfoCreateView(LoginRequiredMixin, ApplicantGeneric, generic.CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'projectx_app/document-form.html'

    def form_valid(self, form):
        form.save(self.request)
        return redirect('document-info-listing')


class DocumentInfoUpdateView(LoginRequiredMixin, ApplicantGeneric, generic.UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'projectx_app/document-form.html'
    success_url = reverse_lazy('document-info-listing')

    # get the object
    def get_object(self, *args, **kwargs):
        doc_info = get_object_or_404(Document, pk=self.kwargs['id'])
        return doc_info

    def form_valid(self, form):
        form.save(self.request)
        return redirect('document-info-listing')


def delete_document_info(request, document_id=None):
    '''
        This function is used to delete document.
    '''
    try:
        delete_document = Document.objects.filter(pk = int(document_id)).update(is_deleted = True)
    except:
        delete_document = None

    if delete_document:
        data = {
            'status': 'true'
        }
    else:
        data = {
            'status': 'false'
        }

    return JsonResponse(data)

