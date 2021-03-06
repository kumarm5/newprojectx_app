# Generated by Django 2.1.4 on 2018-12-31 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0026_vendoruser'),
    ]

    operations = [
        migrations.AddField(
            model_name='myrequesttasksinfo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='myrequesttasksinfo',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requestinfo_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='myrequesttasksinfo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
