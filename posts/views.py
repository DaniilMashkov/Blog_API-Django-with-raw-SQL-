from django.http import Http404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics

from posts.repository.post_repository import PostRepository
from posts.serializers import PostDetailSerializer, PostListSerializer
from posts.service import PostService


@extend_schema(
        parameters=[
            OpenApiParameter(name='author_id', type=int, required=False, description='Filter by author ID'),
            OpenApiParameter(
                name='order_by',
                type=str,
                required=False,
                description='Order by field name',
                enum=['title', 'post_created']
            )
        ]
    )
class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    repo = PostRepository()
    service = PostService(repo)

    def get_queryset(self):
        author_id = self.request.query_params.get('author_id')
        order_by = self.request.query_params.get('order_by', 'created')
        posts = self.service.get_posts(author_id, order_by)

        if not posts:
            raise Http404("Posts not found")

        return posts


class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer
    repo = PostRepository()
    service = PostService(repo)

    def get_object(self):
        post_id = self.kwargs['pk']
        post = self.service.get_post_with_comments(post_id)

        if not post:
            raise Http404("Post not found")

        return post
