# Generated by Django 2.1.4 on 2018-12-22 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0002_auto_20181221_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myrequest',
            name='task',
        ),
        migrations.AddField(
            model_name='myrequest',
            name='co_onboarding_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectx_app.CoOnboardingType'),
        ),
        migrations.AddField(
            model_name='myrequest',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectx_app.SystemCompanySetup'),
        ),
    ]
