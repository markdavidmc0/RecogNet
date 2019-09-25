# Generated by Django 2.2.5 on 2019-09-25 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('male', 'female')], max_length=30)),
                ('unprocessed_video_url', models.URLField()),
                ('processed_video_url', models.URLField()),
                ('unprocessed_image_url', models.URLField()),
                ('processed_image_url', models.URLField()),
                ('modified', models.DateTimeField()),
                ('created', models.DateTimeField(editable=False)),
            ],
        ),
    ]
