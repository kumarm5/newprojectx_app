# Generated by Django 2.1.4 on 2019-02-07 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0086_myrequesttasks_cmo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemcompanysetup',
            name='finance_email',
            field=models.EmailField(blank=True, max_length=256, null=True, verbose_name='Finance Eamil'),
        ),
        migrations.AddField(
            model_name='systemcompanysetup',
            name='finance_user_name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Finance User Name'),
        ),
    ]
