from django.db import models
from django.utils import timezone


class Person(models.Model):
    """Image Recognition person security profile."""
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField
    gender = models.CharField(max_length=30, choices=[('male', 'female')])
    unprocessed_video_url = models.URLField(default='https://console.cloud.google.com/'
                                                    'storage/browser/'
                                                    'recognet-unprocessed-videos/')
    processed_video_url = models.URLField(default='https://console.cloud.google.com/'
                                                  'storage/browser/'
                                                  'recognet-processed-videos/')
    unprocessed_image_url = models.URLField(default='https://console.cloud.google.com/'
                                                    'storage/browser/'
                                                    'recognet-unprocessed-images/')
    processed_image_url = models.URLField(default='https://console.cloud.google.com/'
                                                  'storage/browser/'
                                                  'recognet-processed-images/')
    image = models.FileField(upload_to='')
    modified = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """Update timestamps on save."""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Person, self).save(*args, **kwargs)
