from environs import Env
from google.cloud import storage
from PIL import Image
from resizeimage import resizeimage
from uuid import uuid4

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from recognition_api.models import Person
from recognition_api.serializers import PersonSerializer
from rest_framework.response import Response


env = Env()
env.read_env()  # read .env file, if it exists

BUCKET_NAME_UNPROCESSED = env('BUCKET_NAME_UNPROCESSED')
BUCKET_NAME_PROCESSED = env('BUCKET_NAME_PROCESSED')
SERVICE_ACCOUNT = env('SERVICE_ACCOUNT')


class PredictionViewSet(viewsets.GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin):
    """Person endpoint to interact with Person object."""
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    @action(detail=False, methods=['post'])
    def predict(self, request):
        """Predict whether image received matches person in DB or not."""
        # store incoming image
        unprocessed_name = self.store(request, BUCKET_NAME_UNPROCESSED)
        # process image
        # self.preprocess_file(request)
        # store processed image
        self.store(request, BUCKET_NAME_PROCESSED)
        return Response('')

    def store(self, request, bucket_name):
        """Uploads a file to a bucket."""
        # Instantiates a client
        storage_client = storage.Client.from_service_account_json(SERVICE_ACCOUNT)

        if request.method == 'POST':
            file = request.FILES['image']
            file.seek(0)
            bucket = storage_client.get_bucket(bucket_name)

            # create filename
            destination_blob_name = str(uuid4())
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_file(file)

            print(f'File {destination_blob_name} uploaded to {blob}.')

            return destination_blob_name
        else:
            raise FileNotFoundError()

    @staticmethod
    def preprocess_file(request):
        width = 96
        height = 96
        if request.method == 'POST':
            file = request.FILES['file']
            image = Image.open(file)
            image = resizeimage.resize_cover(image, [width, height])
            # TODO convert from image to bytes-array
            request.FILES['file'] = image
        else:
            pass
