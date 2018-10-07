# -*- coding: utf-8 -*-
import logging
from random import random

from django.contrib.auth.models import User, Group
from django.core.management import BaseCommand
from django.db import transaction

from blog.factories import PostFactory
from blog.models import Post
from blog.permissions import add_permission_to_add_model

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Populate database with users and blog posts"

    @transaction.atomic
    def handle(self, *args, **options):
        # ====================================================================================
        # Users & Groups
        # ====================================================================================
        # create authors group
        authors_group, _ = Group.objects.get_or_create(name='authors')
        add_permission_to_add_model(Post, authors_group)

        # create 2 authors
        alberti, _ = User.objects.get_or_create(username='alberti27', first_name='Rafael', last_name='Alberti')
        if authors_group not in alberti.groups.all():
            alberti.groups.add(authors_group)
        douglas, _ = User.objects.get_or_create(username='douglas42', first_name='Douglas', last_name='Adams')
        if authors_group not in douglas.groups.all():
            douglas.groups.add(authors_group)
        authors = [alberti, douglas]

        # ====================================================================================
        # Posts
        # ====================================================================================
        if Post.objects.count() > 10:
            logger.info('There are {} posts already in DB, not generating more...'.format(Post.objects.count()))
        else:
            for _ in range(42):
                PostFactory(author=authors[int(round(random()))])
