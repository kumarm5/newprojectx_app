# Generated by Django 2.1.4 on 2019-02-05 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0081_coonboardingtaskmedicalform'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyRequestTaskMedicalForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('myrequest_tasks_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myrequest_medical_task', to='projectx_app.MyRequestTasksInfo')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myrequest_medical_templates', to='projectx_app.Template')),
            ],
            options={
                'verbose_name_plural': 'My Request HRs',
                'verbose_name': 'My Request HR',
            },
        ),
    ]
