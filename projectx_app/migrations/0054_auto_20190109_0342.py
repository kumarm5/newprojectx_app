# Generated by Django 2.1.4 on 2019-01-09 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectx_app', '0053_auto_20190109_0327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myrequesttaskshrdocs',
            name='document',
        ),
        migrations.AddField(
            model_name='myrequesttaskshrdocs',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_hr_template', to='projectx_app.Template'),
        ),
    ]