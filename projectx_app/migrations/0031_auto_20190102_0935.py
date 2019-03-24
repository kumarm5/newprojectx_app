# Generated by Django 2.1.4 on 2019-01-02 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0030_auto_20190102_0910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyuser',
            name='created_by',
        ),
        migrations.AddField(
            model_name='companyuser',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='companyuser_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
