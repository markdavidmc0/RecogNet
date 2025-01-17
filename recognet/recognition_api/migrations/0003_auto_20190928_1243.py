# Generated by Django 2.2.5 on 2019-09-28 12:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('recognition_api', '0002_auto_20190928_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 28, 12, 43, 27, 616961, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='person',
            name='processed_image_url',
            field=models.URLField(default='https://console.cloud.google.com/storage/browser/recognet-processed-images/'),
        ),
        migrations.AlterField(
            model_name='person',
            name='processed_video_url',
            field=models.URLField(default='https://console.cloud.google.com/storage/browser/recognet-processed-videos/'),
        ),
        migrations.AlterField(
            model_name='person',
            name='unprocessed_image_url',
            field=models.URLField(default='https://console.cloud.google.com/storage/browser/recognet-unprocessed-images/'),
        ),
        migrations.AlterField(
            model_name='person',
            name='unprocessed_video_url',
            field=models.URLField(default='https://console.cloud.google.com/storage/browser/recognet-unprocessed-videos/'),
        ),
    ]
