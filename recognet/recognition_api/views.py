from rest_framework import viewsets
from recognition_api.models import Person
from recognition_api.serializers import PersonSerializer
from rest_framework.response import Response


class PersonViewSet(viewsets.ModelViewSet):
    """Person endpoint to interact with Person object."""
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def predict(self, data):
        """Predict whether image received matches person in DB or not."""
        return Response(data)
