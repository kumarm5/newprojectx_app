# Generated by Django 2.1.4 on 2019-01-09 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0054_auto_20190109_0342'),
    ]

    operations = [
        migrations.AddField(
            model_name='myrequesttasksrefdocs',
            name='not_applicable',
            field=models.BooleanField(blank=True, null=True, verbose_name='Request Not Applicable'),
        ),
    ]
