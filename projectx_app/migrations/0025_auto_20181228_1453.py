# Generated by Django 2.1.4 on 2018-12-28 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0024_myrequesttasksinfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myrequesttasksbgvdocs',
            old_name='document_name',
            new_name='document_file',
        ),
        migrations.RemoveField(
            model_name='myrequesttasksbgvdocs',
            name='bgv_task_id',
        ),
        migrations.RemoveField(
            model_name='myrequesttasksbgvdocs',
            name='mark_complete',
        ),
        migrations.AddField(
            model_name='myrequesttasks',
            name='mark_complete',
            field=models.BooleanField(default=False, verbose_name='Mark Complete'),
        ),
        migrations.AddField(
            model_name='myrequesttasksbgvdocs',
            name='request_progress_status',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='request_progress_status'),
        ),
        migrations.AddField(
            model_name='myrequesttasksbgvdocs',
            name='request_result_status',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='request_result_status'),
        ),
    ]
