# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, permissions

from blog.models import (
    Post,
    Tag,
)
from blog.permissions import IsAuthorOrReadOnly
from blog.serializers import (
    PostSerializer,
    TagSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all().order_by('-created')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
