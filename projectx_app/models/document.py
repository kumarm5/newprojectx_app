from django.db import models
from django.conf import settings
from projectx_app.models.user import User
from projectx_app.models.master import *


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='document_user')
    document_name = models.ForeignKey(DocumentTypeName, on_delete=models.CASCADE, null=True, blank=True, related_name='document_type_name')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, related_name='counties')
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True, related_name='states')
    name_in_document = models.CharField(max_length=256, null=True, blank=True, verbose_name='Name appear in the document')
    issued_by = models.CharField(max_length=256, null=True, blank=True, verbose_name='Issued By')
    date_of_issue = models.CharField(max_length=256, null=True, blank=True, verbose_name='Date Of Issue')
    valid_till = models.CharField(max_length=256, null=True, blank=True, verbose_name='Valid Till')
    city = models.CharField(max_length=256, null=True, blank=True, verbose_name='City')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name_in_document

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"


class DocumentFiles(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='document')
    file_name = models.FileField(upload_to='document_files/', blank=True, null=True, verbose_name='File Name')

    def __str__(self):
        return self.file_name.name

    class Meta:
        verbose_name = "Document File"
        verbose_name_plural = "Document Files"
