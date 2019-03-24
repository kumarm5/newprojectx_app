# Generated by Django 2.1.4 on 2019-02-05 07:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0083_auto_20190205_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='myrequesttasksinfo',
            name='medical_cmo_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_medical_cmo_user', to=settings.AUTH_USER_MODEL, verbose_name='Medical CMO User'),
        ),
    ]