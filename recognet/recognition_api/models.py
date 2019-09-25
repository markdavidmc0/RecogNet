from django.db import models
from django.utils import timezone


class Person(models.Model):
    """Image Recognition person security profile."""
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField
    gender = models.CharField(max_length=30, choices=[('male', 'female')])
    unprocessed_video_url = models.URLField()
    processed_video_url = models.URLField()
    unprocessed_image_url = models.URLField()
    processed_image_url = models.URLField()
    modified = models.DateTimeField()
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """Update timestamps on save."""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Person, self).save(*args, **kwargs)
