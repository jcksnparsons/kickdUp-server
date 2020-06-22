from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import SneakerPost, Comment
from datetime import datetime
from django.contrib.auth.models import User


class CommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Comment
        url = serializers.HyperlinkedIdentityField(
            view_name="comment",
            lookup_field="id"
        )
        fields = ('id', 'post_id', 'user', 'user_id', 'content', 'create_at')


class Comments(ViewSet):

    def list(self, request):
        comments = Comment.objects.all()
        post = self.request.query_params.get("post", None)
        if post is not None:
            comments = comments.filter(post__id=post)
        serializer = CommentSerializer(
            comments, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.user = User.objects.get(pk=comment.user_id)
            serializer = CommentSerializer(
                comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        new_comment = Comment()

        new_comment.post = SneakerPost.objects.get(pk=request.data["post_id"])
        new_comment.user = request.auth.user
        new_comment.content = request.data["content"]
        new_comment.create_at = datetime.now()

        new_comment.save()

        serializer = CommentSerializer(
            new_comment, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.content = request.data["content"]

            serializer = CommentSerializer(
                comment, context={'request': request}, partial=True)

            comment.save()

            return Response(status=status.HTTP_201_CREATED, data=serializer.data)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
