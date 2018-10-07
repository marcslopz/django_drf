from rest_framework import serializers

from blog.models import (
    Post,
    Tag,
)


class PostSerializerWithDatetime(serializers.ModelSerializer):
    # to use django template filter `date`
    created = serializers.DateTimeField(format=None)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'tags', 'created', 'modified')
        # get author fields from this model
        depth = 1


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'tags', 'created', 'modified')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'description')
