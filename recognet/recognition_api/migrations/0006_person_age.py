# Generated by Django 2.2.5 on 2019-09-28 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recognition_api', '0005_auto_20190928_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='age',
            field=models.IntegerField(default=0),
        ),
    ]
