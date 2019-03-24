# Generated by Django 2.1.4 on 2019-02-02 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0070_auto_20190128_0612'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reimbursement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('co_onboarding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='co_onboarding_reimbursement', to='projectx_app.CoOnboardingType')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reimbursement_owner', to=settings.AUTH_USER_MODEL)),
                ('system_company_setup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_reimbursement', to='projectx_app.SystemCompanySetup')),
            ],
            options={
                'verbose_name_plural': 'Reimbursements',
                'verbose_name': 'Reimbursement',
            },
        ),
    ]