# Generated by Django 2.1.4 on 2019-02-04 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0079_auto_20190204_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='coonboardingtask',
            name='medical_cmo_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_cmo_user', to=settings.AUTH_USER_MODEL, verbose_name='Medical CMO User'),
        ),
        migrations.AlterField(
            model_name='coonboardingtask',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='onboarding_vendor', to='projectx_app.CompanyVendor'),
        ),
    ]
