# Generated by Django 2.1.4 on 2018-12-23 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0003_auto_20181222_0658'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysVendorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_description', models.CharField(choices=[('BGV', 'Back Ground Verification'), ('RFC', 'Reference Check'), ('HRF', 'HR Forms')], max_length=30, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'System Vendor Type',
                'verbose_name_plural': 'System Vendor Types',
            },
        ),
        migrations.CreateModel(
            name='VendorMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_company_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Vendor Company Name')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('vendor_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Vendor Phone Number')),
                ('vendor_admin', models.CharField(blank=True, max_length=256, null=True, verbose_name='Vendor Admin')),
                ('admin_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Vendor Admin Phone Number')),
                ('area_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Vendor Phone Number')),
                ('email', models.EmailField(blank=True, max_length=256, null=True, verbose_name='Email')),
                ('tax_number', models.CharField(blank=True, max_length=256, null=True, verbose_name='Tax Number')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_country', to='projectx_app.Country')),
                ('country_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_country_code', to='projectx_app.CountryCode')),
            ],
            options={
                'verbose_name': 'Document Type Name',
                'verbose_name_plural': 'Document Type Names',
            },
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='email',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='phone_no',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='vendor_id',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='vendor_name',
        ),
        migrations.AddField(
            model_name='vendor',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectx_app.SystemCompanySetup'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='service_provider_type',
            field=models.CharField(blank=True, choices=[('external', 'External'), ('internal', 'Internal')], max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='sys_vendor_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectx_app.SysVendorType', verbose_name='System Vendor Type'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectx_app.VendorMaster'),
        ),
    ]
