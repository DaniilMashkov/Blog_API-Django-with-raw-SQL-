from rest_framework import serializers


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()


class PostListSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()
    image = serializers.ImageField(required=False)
    created = serializers.DateTimeField()
    author = AuthorSerializer()
    last_comment_date = serializers.DateTimeField(required=False)
    last_comment_author = serializers.CharField(required=False)


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = serializers.CharField()
    body = serializers.CharField()
    created = serializers.DateTimeField()


class PostDetailSerializer(serializers.Serializer):
    title = serializers.CharField()
    text = serializers.CharField()
    image = serializers.ImageField()
    created = serializers.DateTimeField()
    author = AuthorSerializer()
    comments = CommentSerializer(many=True)
