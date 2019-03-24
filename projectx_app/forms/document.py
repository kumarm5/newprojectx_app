from django import forms
from projectx_app.models.user import User
from projectx_app.models.document import *
from django.conf import settings
from django.db import transaction
from django.core.files.storage import FileSystemStorage

class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)

        self.fields['document_name'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['country'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['state'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['name_in_document'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['issued_by'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['date_of_issue'].widget.attrs['class'] = 'form-control date-picker r-0 light s-12'
        self.fields['date_of_issue'].widget.attrs['autocomplete'] = 'off'
        self.fields['valid_till'].widget.attrs['class'] = 'form-control date-picker r-0 light s-12'
        self.fields['valid_till'].widget.attrs['autocomplete'] = 'off'
        self.fields['city'].widget.attrs['class'] = 'form-control r-0 light s-12'

    class Meta:
        model = Document
        fields = ('__all__')

    @transaction.atomic
    def save(self, request, commit=True):
        instance = super(DocumentForm, self).save(commit=False)

        DocumentFiles.objects.filter(document = instance).delete()

        if commit:
            instance.save()
            if request.FILES:
                for myfile in request.FILES.getlist('file_name'):
                    DocumentFiles.objects.create(file_name=myfile, document=instance)

        return instance


class DocumentFilesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentFilesForm, self).__init__(*args, **kwargs)

        self.fields['document'].widget.attrs['class'] = 'form-control r-0 light s-12'
        self.fields['file_name'].widget.attrs['class'] = 'form-control r-0 light s-12'

    class Meta:
        model = DocumentFiles
        fields = ('__all__')
