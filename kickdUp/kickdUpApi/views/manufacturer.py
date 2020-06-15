from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kickdUpApi.models import Manufacturer

class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Manufacturer
        url = serializers.HyperlinkedIdentityField(
            view_name="manufacturer",
            lookup_field="id"
        )
        fields =('id', 'name')

class Manufacturers(ViewSet):
    def retrieve(self, request, pk=None):
            manufacturer = Manufacturer.objects.get(pk=pk)
            serializer = ManufacturerSerializer(manufacturer, context={'request': request})
            return Response(serializer.data)

    def list(self, request):
            manufacturers = Manufacturer.objects.all()
            serializer = ManufacturerSerializer(manufacturers, many=True, context={'request': request})
            return Response(serializer.data)