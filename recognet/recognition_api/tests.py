from environs import Env
from PIL import Image

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from recognition_api.models import Person
from recognition_api.views import PersonViewSet


class PersonTestCase(TestCase):
    """Test class for the Person Model."""
    factory = APIRequestFactory()

    def test_person(self):
        """Person."""
        request = self.factory.post('/notes/', {'title': 'new idea'})
        with open("/Users/markmc/Repos/RecogNet/recognet/recognition_api/test_files/"
                  "mark_03.jpg", "rb") as image:
            response = PersonViewSet.predict(PersonViewSet(), request)
        x = 5