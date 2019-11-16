"""Viewsets for prediction API."""

from environs import Env
from google.cloud import storage
from io import BytesIO
from PIL import Image
from resizeimage import resizeimage
from uuid import uuid4

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from recognition_api.models import Person
from recognition_api.serializers import PersonSerializer
from rest_framework.response import Response


env = Env()
env.read_env()  # read .env file, if it exists

BUCKET_NAME_UNPROCESSED = env('BUCKET_NAME_UNPROCESSED')
BUCKET_NAME_PROCESSED = env('BUCKET_NAME_PROCESSED')
SERVICE_ACCOUNT = env('SERVICE_ACCOUNT')
WIDTH = int(env('WIDTH'))
HEIGHT = int(env('HEIGHT'))


class PersonViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin):
    """Person endpoint to interact with Person object."""
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    file_name = ''
    public_url = []

    @action(detail=False, methods=['post'])
    def predict(self, request) -> Response:
        """Predict whether image received matches person in DB or not.
        :param request: DRF HttpRequest"""
        # store incoming image
        self.store(request, BUCKET_NAME_UNPROCESSED)
        # process image
        self.preprocess_image(request)
        # store processed image
        self.store(request, BUCKET_NAME_PROCESSED)

        return Response(
            {
                'unprocessed_image': self.public_url[0],
                'processed_image': self.public_url[1]
            })

    def store(self, request, bucket_name) -> None:
        """Uploads a file to a bucket.
        :param request: DRF HttpRequest
        :param bucket_name: str"""
        if request.method == 'POST':
            file = request.FILES['image']
            file.seek(0)
            if not self.file_name:
                self.file_name = str(uuid4())
            # get Person image folder - defaults to match Model fields
            person = self.get_person(request)

            # determine blob name based on person image is associated with
            destination_blob_name = person + '/' + self.file_name

            # file upload via GCS API
            blob = self.upload_to_gcs(file, bucket_name, destination_blob_name)
            self.public_url.append(blob)
            print(f'File {destination_blob_name} uploaded to {blob}')
        else:
            raise MethodNotAllowed(request.method,
                                   detail="file upload won't occur unless POST")

    def get_person(self, request) -> str:
        """Get unique identifier for person from Model.
        :param request: DRF HttpRequest
        """
        if self.get_queryset():
            person = str(self.get_queryset().filter(
                first_name=request.data.get('first_name', 'unknown'),
                last_name=request.data.get('last_name', 'unknown'),
                year_of_birth=request.data.get('year_of_birth', 0),
                location=request.data.get('location', 'unknown')))
        else:
            person = 'unknown_unknown_0_unknown'

        return person

    @staticmethod
    def upload_to_gcs(file, bucket_name, destination_blob_name):
        """Upload file via GCS API.
        :param file: file handle (bytes) or BytesIO
        :param bucket_name: str
        :param destination_blob_name: str"""
        storage_client = storage.Client.from_service_account_json(SERVICE_ACCOUNT)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_file(file)

        return blob.public_url

    @staticmethod
    def preprocess_image(request) -> None:
        """Transform image with PIL and resizeimage.

        File saved as BytesIO to request.FILES['image] - this is NB
        :param request: DRF HttpRequest"""
        if request.method == 'POST':
            file = request.FILES['image']
            image = Image.open(file)
            image = resizeimage.resize_cover(image, [WIDTH, HEIGHT])
            output = BytesIO()
            image.save(output, format="JPEG")
            request.FILES['image'] = output
        else:
            raise MethodNotAllowed(request.method,
                                   detail="file upload won't occur unless POST")
