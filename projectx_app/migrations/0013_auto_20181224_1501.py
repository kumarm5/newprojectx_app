# Generated by Django 2.1.4 on 2018-12-24 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0012_auto_20181224_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='service_provider_type',
            field=models.CharField(blank=True, choices=[('external', 'External'), ('internal', 'Internal')], default='external', max_length=256, null=True),
        ),
    ]
