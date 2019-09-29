from django.db import models
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
    unprocessed_video_url = models.URLField(default=unprocessed_video_url_env)
    processed_video_url = models.URLField(default=processed_video_url_env)
    unprocessed_image_url = models.URLField(default=unprocessed_image_url_env)
    processed_image_url = models.URLField(default=processed_image_url_env)
    modified = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """Updates on save."""
        # timestamps
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()

        # urls
        self.unprocessed_video_url = '_'.join(
            [
                self.unprocessed_video_url,
                self.first_name,
                self.last_name,
                str(self.year_of_birth),
                self.location
            ]
        )
        self.processed_video_url = '_'.join(
            [
                self.processed_video_url,
                self.first_name,
                self.last_name,
                str(self.year_of_birth),
                self.location
            ]
        )
        self.unprocessed_image_url = '_'.join(
            [
                self.unprocessed_image_url,
                self.first_name,
                self.last_name,
                str(self.year_of_birth),
                self.location
            ]
        )
        self.processed_image_url = '_'.join(
            [
                self.processed_image_url,
                self.first_name,
                self.last_name,
                str(self.year_of_birth),
                self.location
            ]
        )
        return super(Person, self).save(*args, **kwargs)
