# Generated by Django 3.2.6 on 2021-11-29 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AnalyticsPlatformApi', '0002_alter_processed_video_processed_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processed_video',
            name='source_type',
            field=models.CharField(max_length=200),
        ),
    ]
