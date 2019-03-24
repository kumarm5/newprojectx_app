# Generated by Django 2.1.4 on 2019-01-06 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0049_auto_20190105_0546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myrequesttasksbgvdocs',
            name='request_progress_status',
        ),
        migrations.RemoveField(
            model_name='myrequesttasksbgvdocs',
            name='request_result_status',
        ),
        migrations.AddField(
            model_name='myrequesttasksbgvdocs',
            name='mark_complete',
            field=models.BooleanField(blank=True, null=True, verbose_name='Request Mark Complete'),
        ),
        migrations.AddField(
            model_name='myrequesttasksbgvdocs',
            name='not_applicable',
            field=models.BooleanField(blank=True, null=True, verbose_name='Request Not Applicable'),
        ),
    ]