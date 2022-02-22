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

        latest_post = Post.objects.first()
        self.assertEqual(latest_post.text, form_data['text'])
        self.assertEqual(latest_post.author, self.author)
        self.assertEqual(latest_post.group, self.group)

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
        edit_post = Post.objects.get(id=self.post.id)
        self.assertEqual(edit_post.text, form_data['text'])
        self.assertEqual(edit_post.author, self.author)
        self.assertEqual(edit_post.group, self.group)

    def test_guest_client_could_not_create_posts(self):
        posts_before = Post.objects.count()
        form_data = {
            'group': self.group.id,
            'text': 'editted_text',
            'author': self.guest_client,
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        expected_redirect = str(reverse('users:login') + '?next='
                                + reverse('posts:post_create'))
        self.assertRedirects(response, expected_redirect)
        self.assertEqual(Post.objects.count(), posts_before)
