from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


from ..models import Group, Post

User = get_user_model()


class PostFormsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

        cls.user = User.objects.create_user(username='user')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.author = User.objects.create_user(username='author')
        cls.authorized_author = Client()
        cls.authorized_author.force_login(cls.author)

        cls.group = Group.objects.create(
            title='test_title',
            slug='test_slug',
            description='test_descrioption'
        )

        cls.post = Post.objects.create(
            text='Тестовый пост',
            group=cls.group,
            author=cls.author
        )

    def test_create_post(self):
        posts_count = Post.objects.count()

        form_data = {
            'text': 'new_text',
            'group': self.group.id,
            'username': self.author.username,
        }

        response = self.authorized_author.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(
            response, reverse('posts:profile', args=[self.author])
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)

        self.assertTrue(
            Post.objects.filter(
                group=self.group,
                text='new_text',
                author=self.author,
            ).exists()
        )

    def test_edit_post(self):
        form_data = {
            'post_id': self.post.id,
            'text': 'editted_text',
            'group': self.group.id,
            'author': self.author,
        }
        response = self.authorized_author.post(
            reverse('posts:post_edit', args=[self.post.id]),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, reverse('posts:post_detail', args=[self.post.id])
        )
        edit_post = Post.objects.latest('id')
        self.assertEqual(edit_post.text, 'editted_text')
        self.assertEqual(edit_post.author, self.author)
        self.assertEqual(edit_post.group, self.group)