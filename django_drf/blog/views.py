# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from blog.models import (
    Post,
    Tag,
)
from blog.serializers import (
    PostSerializer,
    TagSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all().order_by('-modified')
    serializer_class = PostSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
