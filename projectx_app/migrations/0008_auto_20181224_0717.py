# Generated by Django 2.1.4 on 2018-12-24 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0007_auto_20181224_0553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addressinfo',
            name='contact',
        ),
        migrations.AddField(
            model_name='addressinfo',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_address_info', to=settings.AUTH_USER_MODEL),
        ),
    ]
