from io import BytesIO
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import viewsets

from recognition_api.views import PredictionViewSet


class PersonTestCase(APITestCase):
    """Test class for the Person Model."""
    factory = APIRequestFactory()

    def test_person(self):
        """Person."""
        url = reverse('person-predict')
        image = BytesIO()
        with open("/Users/markmc/Repos/RecogNet/recognet/recognition_api/test_files/"
                  "mark_03.jpg", 'rb') as file:
            image.write(file.read())
            image.name = 'test_file.jpg'
        # uploaded_file = InMemoryUploadedFile(
        #     file=memory_file,
        #     field_name='photo',
        #     name='test.jpg',
        #     content_type='application/json',
        #     size=None,
        #     charset=None,
        # )

        data = {'first_name': 'Mark', 'last_name': 'Mc Naught', 'image': image}
        response = self.client.post(url, data)
        # request = self.factory.post(
        #     '/predict/', {'first_name': 'Mark'},
        #     content_type='application/json'
        # )

        # request.FILES['image'] = uploaded_file
        # response = PredictionViewSet.create(PredictionViewSet(), request)
        x = 5