# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.test import TestCase, Client

from blog.factories import PostFactory
from blog.models import Post
from blog.serializers import PostSerializer


class PostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.initial_post_count = 10
        for i in range(self.initial_post_count):
            PostFactory()

    def tearDown(self):
        Post.objects.all().delete()
        pass

    def test_get_list(self):
        response = self.client.get('/posts/')

        self.assertEqual(200, response.status_code)

        content = json.loads(response.content)

        self.assertEqual(self.initial_post_count, len(content))

    def _get_post_by_id(self, post_id):
        """

        :param id: post id to be returned
        :return: tuple (Post, status_code)
        if post id does not exist: (None, 404)
        else: (<PostSerializer instance>, 200)
        """
        response = self.client.get('/posts/{}/'.format(post_id))

        if response.status_code == 404:
            return None, 404
        else:
            serializer = PostSerializer(data=json.loads(response.content))
            self.assertTrue(serializer.is_valid())
            return serializer, response.status_code

    def test_get_details(self):
        for post_id in range(1, self.initial_post_count + 2):
            post_serializer, status_code = self._get_post_by_id(post_id)
            if post_id <= self.initial_post_count:
                self.assertEqual(200, status_code)
                self.assertEqual(post_id, post_serializer.initial_data.get('id'))
            else:
                self.assertEqual(404, status_code)

    def test_create(self):
        new_post = PostFactory()
        # delete from DB
        new_post.delete()

        self.assertEqual(self.initial_post_count, Post.objects.count())

        serializer = PostSerializer(new_post)
        response = self.client.post('/posts/', data=serializer.data)

        self.assertEqual(201, response.status_code)
        self.assertEqual(self.initial_post_count + 1, Post.objects.count())

    def test_delete(self):
        response = self.client.delete('/posts/{}/'.format(self.initial_post_count))

        self.assertEqual(204, response.status_code)
        self.assertEqual(self.initial_post_count - 1, Post.objects.count())

    def test_update(self):
        updated_post = Post.objects.get(id=self.initial_post_count)
        updated_post.title += '...'

        serializer = PostSerializer(updated_post)
        response = self.client.patch(
            '/posts/{}/'.format(self.initial_post_count),
            data=json.dumps(serializer.data),
            content_type='application/json',
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.initial_post_count, Post.objects.count())

        db_updated_post = Post.objects.get(id=self.initial_post_count)
        self.assertEqual(updated_post, db_updated_post)