# Generated by Django 2.1.4 on 2018-12-24 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0013_auto_20181224_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysvendortype',
            name='type_description',
            field=models.CharField(max_length=30, verbose_name='Description'),
        ),
    ]
