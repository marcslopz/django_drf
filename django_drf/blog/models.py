# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(TimestampedModel):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120, null=True, blank=True)


class Post(TimestampedModel):
    title = models.CharField(max_length=120)
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, related_name="tags", blank=True)
