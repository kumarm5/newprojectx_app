# Generated by Django 2.1.4 on 2019-02-12 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0093_auto_20190211_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='myrequesttasksinfo',
            name='is_cmo_action',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Is CMO Actioned'),
        ),
    ]
