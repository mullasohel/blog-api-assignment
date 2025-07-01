from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date
from .models import Post, Author
from .serializers import PostSerializer, AuthorSerializer
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            author = request.query_params.get('author')
            created_at = request.query_params.get('created_at')
            posts = Post.objects.all()

            if author:
                posts = posts.filter(author__name__icontains=author)
            if created_at:
                try:
                    date_obj = parse_date(created_at)
                    posts = posts.filter(created_at__date=date_obj)
                except Exception:
                    return Response({'error': 'Invalid date format.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=PostSerializer)
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                channel_layer = get_channel_layer()
                if channel_layer:
                    async_to_sync(channel_layer.group_send)(
                        'posts',
                        {
                            'type': 'new_post_notification',
                            'content': {'message': f"New post added: {serializer.data['title']}"}
                        }
                    )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        try:
            post = self.get_object(pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=PostSerializer)
    def put(self, request, pk):
        try:
            post = self.get_object(pk)
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=PostSerializer)
    def patch(self, request, pk):
        try:
            post = self.get_object(pk)
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(responses={204: 'Post deleted successfully'})
    def delete(self, request, pk):
        try:
            post = self.get_object(pk)
            post.delete()
            return Response({'message': 'Post deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AuthorListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=AuthorSerializer)
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
