import os
from environs import Env
from google.cloud import storage
from resizeimage import resizeimage

from rest_framework import viewsets
from recognition_api.models import Person
from recognition_api.serializers import PersonSerializer
from rest_framework.response import Response


env = Env()
env.read_env()  # read .env file, if it exists

BUCKET_NAME_UNPROCESSED = env('BUCKET_NAME_UNPROCESSED')
BUCKET_NAME_PROCESSED = env('BUCKET_NAME_PROCESSED')
SERVICE_ACCOUNT = env('SERVICE_ACCOUNT')


class PersonViewSet(viewsets.ModelViewSet):
    """Person endpoint to interact with Person object."""
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def predict(self, request):
        """Predict whether image received matches person in DB or not."""
        # store incoming image
        unprocessed_name = self.store(request, BUCKET_NAME_UNPROCESSED)
        # process image
        processed_image = self.preprocess_file(unprocessed_name)
        # store processed image
        self.store(request, BUCKET_NAME_PROCESSED)
        return Response('')

    @staticmethod
    def store(request, bucket_name):
        """Uploads a file to a bucket."""
        # Instantiates a client
        storage_client = storage.Client.from_service_account_json(SERVICE_ACCOUNT)

        if request.method == 'POST':
            file = request.FILES['file']
            bucket = storage_client.get_bucket(bucket_name)
            source_filename = file.name.split('/')[-1]
            destination_blob_name = source_filename
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_file(file)

            print(f'File {source_filename} uploaded to {destination_blob_name}.')
            return destination_blob_name
        else:
            raise FileNotFoundError()

    @staticmethod
    def preprocess_file(image):
        width = 96
        height = 96
        return resizeimage.resize_cover(image, [width, height]),
