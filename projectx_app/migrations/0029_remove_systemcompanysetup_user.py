# Generated by Django 2.1.4 on 2019-01-02 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0028_auto_20181231_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='systemcompanysetup',
            name='user',
        ),
    ]