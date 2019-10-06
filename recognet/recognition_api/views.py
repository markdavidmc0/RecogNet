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

        return Response(f'unprocessed image successfully uploaded to:'
                        f' {BUCKET_NAME_UNPROCESSED + self.file_name} | '
                        f'processed image successfully uploaded to'
                        f' {BUCKET_NAME_PROCESSED + self.file_name}.')

    def store(self, request, bucket_name) -> None:
        """Uploads a file to a bucket.
        :param request: DRF HttpRequest
        :param bucket_name: str"""
        if request.method == 'POST':
            file = request.FILES['image']
            file.seek(0)
            if not self.file_name:
                self.file_name = str(uuid4())
            destination_blob_name = self.file_name

            # file upload via GCS API
            blob = self.upload_to_gcs(file, bucket_name, destination_blob_name)
            print(f'File {destination_blob_name} uploaded to {blob}.')
        else:
            raise MethodNotAllowed(request.method,
                                   detail="file upload won't occur unless POST")

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

        return blob

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
