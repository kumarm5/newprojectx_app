# Generated by Django 2.1.4 on 2019-02-18 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0101_auto_20190215_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='coonboardingtask',
            name='send_to_candidate',
            field=models.BooleanField(default=False),
        ),
    ]