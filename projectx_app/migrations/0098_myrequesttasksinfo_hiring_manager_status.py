# Generated by Django 2.1.4 on 2019-02-14 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0097_myrequesttasksinfo_hiring_manager_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='myrequesttasksinfo',
            name='hiring_manager_status',
            field=models.CharField(blank=True, choices=[('Approve', 'Approve'), ('Reject', 'Reject')], default='Reject', max_length=100, null=True),
        ),
    ]