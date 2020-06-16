from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Following
from django.contrib.auth.models import User


class FollowingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Following
        url = serializers.HyperlinkedIdentityField(
            view_name="following",
            lookup_field="id"
        )
        fields = ('id', 'user_id', 'following_id')


class Followings(ViewSet):

    def list(self, request):
        followings = Following.objects.all()
        serializer = FollowingSerializer(
            followings, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            following = Following.objects.get(pk=pk)
            serializer = FollowingSerializer(
                following, context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        new_following = Following()

        new_following.user = request.auth.user
        new_following.following = User.objects.get(pk=request.data["following_id"])

        new_following.save()

        serializer = FollowingSerializer(
            new_following, context={'request': request}
        )
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            following = Following.objects.get(pk=pk)
            following.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Following.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
