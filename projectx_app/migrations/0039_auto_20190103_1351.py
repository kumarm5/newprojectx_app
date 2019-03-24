# Generated by Django 2.1.4 on 2019-01-03 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0038_medicalcheck'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalcheck',
            name='attached_template',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Attached Template'),
        ),
        migrations.AddField(
            model_name='medicalcheck',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='Comments'),
        ),
    ]