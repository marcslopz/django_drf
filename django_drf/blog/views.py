# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from blog.models import (
    Post,
    Tag,
)
from blog.permissions import IsAuthorOrReadOnly
from blog.serializers import (
    PostSerializer,
    TagSerializer,
    PostSerializerWithDatetime)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all().order_by('-created')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    template_name = None

    def _is_rendered(self):
        return bool(self.request.query_params.get('render'))

    def get_renderers(self):
        if self._is_rendered():
            return [TemplateHTMLRenderer()]
        else:
            return super(PostViewSet, self).get_renderers()

    def get_serializer_class(self):
        if self._is_rendered():
            self.serializer_class = PostSerializerWithDatetime
        else:
            self.serializer_class = PostSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        self.template_name = 'list.html'
        return super(PostViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.template_name = 'detail.html'
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
