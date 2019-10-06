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
    image = models.ImageField(upload_to='')
    modified = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self) -> str:
        """Set string of model object to unique person identifier."""
        return '_'.join(
            [
                self.first_name,
                self.last_name,
                str(self.year_of_birth),
                self.location
            ]
        )

    def save(self, *args, **kwargs) -> None:
        """Modify save to allow collection of multiple photos per unique person."""
        # .lower for Char fields
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        self.location = self.location.lower()

        # update timestamps
        self.modified = timezone.now()

        # if model exists in DB, update date modified else don't save model
        model = Person.objects.filter(
            first_name=self.first_name,
            last_name=self.last_name,
            year_of_birth=self.year_of_birth,
            location=self.location
        )
        if not model:
            self.init_urls()
            return super(Person, self).save(*args, **kwargs)

    def init_urls(self) -> None:
        """Initialise urls when creating unique person media storage location."""
        unique_id = '_'.join(
            [
                self.first_name,
                self.last_name,
                str(self.year_of_birth),
                self.location
            ]
        )
        self.unprocessed_video_url = self.unprocessed_video_url + unique_id
        self.processed_video_url = self.processed_video_url + unique_id
        self.unprocessed_image_url = self.unprocessed_image_url + unique_id
        self.processed_image_url = self.processed_image_url + unique_id
