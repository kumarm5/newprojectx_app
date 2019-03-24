# Generated by Django 2.1.4 on 2019-01-03 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0032_systemcompanysetup_logo_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Vendor',
            new_name='CompanyVendor',
        ),
        migrations.RemoveField(
            model_name='vendormaster',
            name='user',
        ),
        migrations.AlterField(
            model_name='coonboardingtask',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='onboarding_vendor', to='projectx_app.VendorUser'),
        ),
        migrations.AlterField(
            model_name='myrequesttasks',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_request_vendor', to='projectx_app.VendorUser'),
        ),
        migrations.AlterField(
            model_name='myrequesttasksinfo',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requestinfo_vendor', to='projectx_app.VendorUser'),
        ),
    ]