from django.db import models
from django.db.models.functions import Concat
from django.utils import timezone


unprocessed_video_url_env = 'https://console.cloud.google.com/storage/browser/' \
                            'recognet-unprocessed-videos/'
processed_video_url_env = 'https://console.cloud.google.com/storage/browser/' \
                          'recognet-processed-videos/'
unprocessed_image_url_env = 'https://console.cloud.google.com/storage/browser/' \
                            'recognet-unprocessed-images/'
processed_image_url_env = 'https://console.cloud.google.com/storage/browser/' \
                            'recognet-processed-images/'


class Person(models.Model):
    """Image recognition person security profile."""
    first_name = models.CharField(max_length=30, default='unknown')
    last_name = models.CharField(max_length=30, default='unknown')
    year_of_birth = models.IntegerField(default=0)
    location = models.CharField(max_length=30, default='unknown')
    gender = models.CharField(max_length=30, choices=[('male', 'female')],
                              default='unknown')
    person_unprocessed_video_url = Concat(unprocessed_video_url_env, first_name, '_',
                                          last_name, '_', year_of_birth, '_', location)
    person_processed_video_url = Concat(processed_video_url_env, first_name, '_',
                                        last_name, '_', year_of_birth, '_', location)
    person_unprocessed_image_url = Concat(unprocessed_image_url_env, first_name, '_',
                                          last_name, '_', year_of_birth, '_', location)
    person_processed_image_url = Concat(processed_video_url_env, first_name, '_',
                                        last_name, '_', year_of_birth, '_', location)

    unprocessed_video_url = models.URLField(default=unprocessed_video_url_env)
    processed_video_url = models.URLField(default=processed_video_url_env)
    unprocessed_image_url = models.URLField(default=unprocessed_image_url_env)
    processed_image_url = models.URLField(default=processed_image_url_env)
    modified = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """Update timestamps on save."""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Person, self).save(*args, **kwargs)
