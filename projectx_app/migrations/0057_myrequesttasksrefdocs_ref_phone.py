# Generated by Django 2.1.4 on 2019-01-09 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0056_myrequesttasksrefdocs_row_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='myrequesttasksrefdocs',
            name='ref_phone',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]