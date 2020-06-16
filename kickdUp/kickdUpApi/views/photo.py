from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from ..models import SneakerPost, Photo


class PhotoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Photo
        url = serializers.HyperlinkedIdentityField(
            view_name="photo",
            lookup_field="id"
        )
        fields = ("id", 'image', 'post_id')


class Photos(ViewSet):

    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def list(self, request):
        photos = Photo.objects.all()
        serializer = PhotoSerializer(
            photos, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            photo = Photo.objects.get(pk=pk)
            serializer = PhotoSerializer(
                photo, context={'request': request}
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        new_photo = Photo()

        post = SneakerPost.objects.get(pk=request.data["post_id"])

        new_photo.post = post

        new_photo.image = request.data["image"]

        new_photo.save()

        serializer = PhotoSerializer(
            new_photo, context={'request': request}
        )

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            photo = Photo.objects.get(pk=pk)
            serializer = PhotoSerializer(photo, context={
                'request': request
            })
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
