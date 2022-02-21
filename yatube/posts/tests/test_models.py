from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.group = Group.objects.create(
            title='test_title',
            slug='test_slug',
            description='test_descrioption',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )


    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        groups = PostModelTest.group
        correct_object_names = groups.title
        posts = PostModelTest.post
        correct_object_names = groups.title
        self.assertEqual(correct_object_names, str(groups), str(posts))