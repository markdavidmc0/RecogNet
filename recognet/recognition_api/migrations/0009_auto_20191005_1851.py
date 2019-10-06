# Generated by Django 2.2.5 on 2019-10-05 18:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recognition_api', '0008_auto_20190929_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='image',
            field=models.ImageField(default='empty', upload_to=''),
        ),
        migrations.AlterField(
            model_name='person',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
