# Generated by Django 2.2.5 on 2019-11-16 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recognition_api', '0009_auto_20191005_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
