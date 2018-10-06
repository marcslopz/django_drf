# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.test import TestCase, Client

from blog.factories import PostFactory, TagFactory
from blog.models import Post, Tag
from blog.serializers import PostSerializer, TagSerializer


class BaseCrudTestCase(TestCase):
    # must be overridden
    model_class = None
    root_path = None
    factory_class = None
    serializer_class = None
    model_str_attr_name = None


def _set_up(test_case):
    test_case.client = Client()
    test_case.initial_instance_count = 10
    for i in range(test_case.initial_instance_count):
        test_case.factory_class()


def _tear_down(test_case):
    test_case.model_class.objects.all().delete()
    pass


def _test_get_list(test_case):
    response = test_case.client.get('/{root_path}/'.format(root_path=test_case.root_path))

    test_case.assertEqual(200, response.status_code)

    content = json.loads(response.content)

    test_case.assertEqual(test_case.initial_instance_count, len(content))


def _get_instance_by_id(test_case, instance_id):
    """

    :param instance_id: instance id to be returned
    :return: tuple (model_class, status_code)
    if post id does not exist: (None, 404)
    else: (<model_serializer instance>, 200)
    """
    response = test_case.client.get(
        '/{root_path}/{instance_id}/'.format(root_path=test_case.root_path, instance_id=instance_id))

    if response.status_code == 404:
        return None, 404
    else:
        serializer = test_case.serializer_class(data=json.loads(response.content))
        test_case.assertTrue(serializer.is_valid())
        return serializer, response.status_code


def _test_get_details(test_case):
    for instance_id in range(1, test_case.initial_instance_count + 2):
        serializer, status_code = _get_instance_by_id(test_case, instance_id)
        if instance_id <= test_case.initial_instance_count:
            test_case.assertEqual(200, status_code)
            test_case.assertEqual(instance_id, serializer.initial_data.get('id'))
        else:
            test_case.assertEqual(404, status_code)


def _test_create(test_case):
    new_instance = test_case.factory_class()
    # delete from DB
    new_instance.delete()

    test_case.assertEqual(test_case.initial_instance_count, test_case.model_class.objects.count())

    serializer = test_case.serializer_class(new_instance)
    response = test_case.client.post('/{root_path}/'.format(root_path=test_case.root_path), data=serializer.data)

    test_case.assertEqual(201, response.status_code)
    test_case.assertEqual(test_case.initial_instance_count + 1, test_case.model_class.objects.count())


def _test_delete(test_case):
    response = test_case.client.delete(
        '/{root_path}/{instance_id}/'.format(root_path=test_case.root_path, instance_id=test_case.initial_instance_count))

    test_case.assertEqual(204, response.status_code)
    test_case.assertEqual(test_case.initial_instance_count - 1, test_case.model_class.objects.count())


def _test_update(test_case):
    updated_instance = test_case.model_class.objects.get(id=test_case.initial_instance_count)
    old_attr_value = getattr(updated_instance, test_case.model_str_attr_name)
    new_attr_value = old_attr_value + '...'
    setattr(updated_instance, test_case.model_str_attr_name, new_attr_value)

    serializer = test_case.serializer_class(updated_instance)
    response = test_case.client.patch(
        '/{root_path}/{instance_id}/'.format(root_path=test_case.root_path, instance_id=test_case.initial_instance_count),
        data=json.dumps(serializer.data),
        content_type='application/json',
    )

    test_case.assertEqual(200, response.status_code)
    test_case.assertEqual(test_case.initial_instance_count, test_case.model_class.objects.count())

    db_updated_instance = test_case.model_class.objects.get(id=test_case.initial_instance_count)
    test_case.assertEqual(updated_instance, db_updated_instance)


class PostCrudTestCase(TestCase):
    # must be overridden
    model_class = Post
    root_path = 'posts'
    factory_class = PostFactory
    serializer_class = PostSerializer
    model_str_attr_name = 'title'

    def setUp(self):
        _set_up(self)

    def tearDown(self):
        _tear_down(self)

    def test_get_list(self):
        _test_get_list(self)

    def test_get_details(self):
        _test_get_details(self)

    def test_create(self):
        _test_create(self)

    def test_delete(self):
        _test_delete(self)

    def test_update(self):
        _test_update(self)


class TagCrudTestCase(TestCase):
    # must be overridden
    model_class = Tag
    root_path = 'tags'
    factory_class = TagFactory
    serializer_class = TagSerializer
    model_str_attr_name = 'description'

    def setUp(self):
        _set_up(self)

    def tearDown(self):
        _tear_down(self)

    def test_get_list(self):
        _test_get_list(self)

    def test_get_details(self):
        _test_get_details(self)

    def test_create(self):
        _test_create(self)

    def test_delete(self):
        _test_delete(self)

    def test_update(self):
        _test_update(self)
