# Generated by Django 2.1.4 on 2019-02-14 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0096_auto_20190213_0715'),
    ]

    operations = [
        migrations.AddField(
            model_name='myrequesttasksinfo',
            name='hiring_manager_comment',
            field=models.TextField(blank=True, null=True, verbose_name='Hiring Manager Comments'),
        ),
    ]