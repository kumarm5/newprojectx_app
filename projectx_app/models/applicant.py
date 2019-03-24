from django.db import models
from django.conf import settings
from projectx_app.models.user import User
from projectx_app.models.master import *


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"
