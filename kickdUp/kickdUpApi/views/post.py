from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import SneakerPost, Manufacturer
from datetime import datetime


class PostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SneakerPost
        url = serializers.HyperlinkedIdentityField(
            view_name="post",
            lookup_field="id"
        )
        fields = ('id', 'manufacturer', 'model', 'colorway',
                  'description', 'create_at', 'user')
        depth = 1


class Posts(ViewSet):

    def list(self, request):
        posts = SneakerPost.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            post = SneakerPost.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        new_post = SneakerPost()

        new_post.model = request.data["model"]
        new_post.colorway = request.data["colorway"]
        new_post.description = request.data["description"]
        new_post.create_at = datetime.now()

        new_post.user = request.auth.user

        manufacturer = Manufacturer.objects.get(
            pk=request.data["manufacturer_id"])

        new_post.manufacturer = manufacturer

        new_post.save()

        serializer = PostSerializer(new_post, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk=None):
        try:
            post = SneakerPost.objects.get(pk=pk)
            post.description = request.data["description"]

            serializer = PostSerializer(
                post, context={'request': request}, partial=True)

            post.save()

            return Response(status=status.HTTP_201_CREATED, data=serializer.data)

        except SneakerPost.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            post = SneakerPost.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except SneakerPost.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
