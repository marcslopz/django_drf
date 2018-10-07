import random
import string

import factory
from faker import Factory as Fake
from django.contrib.auth.models import User, Group


faker = Fake.create()


def random_email():
    handle, domain = faker.email().split("@", 2)
    return handle + '.' + rand_string() + "@" + domain


def rand_string(length=6):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def random_username():
    return faker.user_name() + "_" + rand_string()


def random_groupname():
    return faker.group_name() + "_" + rand_string()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda o: random_username())
    first_name = factory.LazyAttribute(lambda o: faker.first_name())
    last_name = factory.LazyAttribute(lambda o: faker.last_name())
    email = factory.LazyAttribute(lambda o: random_email())


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.LazyAttribute(lambda o: random_groupname())
