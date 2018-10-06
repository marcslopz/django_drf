import factory
from faker import Factory as Fake

from blog.models import (
    Post,
    Tag,
)
from users.factories import UserFactory


faker = Fake.create()


class PostFactory(factory.django.DjangoModelFactory):
    title = factory.LazyAttribute(lambda n: faker.sentence(nb_words=3))
    content = factory.LazyAttribute(lambda n: faker.sentence(nb_words=20))
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Post

    @factory.post_generation
    def related(self, create, extracted, **kwargs):
        if not create:
            return
        if kwargs.get('tag', False):
            self.tags.add(TagFactory())


class TagFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda n: faker.sentence(nb_words=1))
    description = factory.LazyAttribute(lambda n: faker.sentence(nb_words=5))

    class Meta:
        model = Tag
