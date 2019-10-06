from unittest import mock

from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase


class PersonTestCase(APITestCase):
    """Test class for the Person Model."""
    factory = APIRequestFactory()

    @mock.patch('recognition_api.views.PersonViewSet.upload_to_gcs')
    def test_viewset(self, mock_upload):
        """Test successful file pre-processing and viewset runs without error."""
        mock_upload.return_value = 'test_blob'
        url = reverse('person-predict')
        with open("/Users/markmc/Repos/RecogNet/recognet/recognition_api/test_files/"
                  "mark_07.jpg", 'rb') as image:
            data = {'first_name': 'Mark', 'last_name': 'Mc Naught', 'image': image}
            response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
