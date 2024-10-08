from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import BlogPost, Category, Tag

User = get_user_model()

class TestSetup(APITestCase):
  
    def setUp(self):
        self.user_profile = reverse('register')
        self.post_create_url = reverse('post-create')
        self.post_update_url_template = 'post-update'
        self.post_delete_url_template = 'post-delete'
        self.valid_post_data = {
            "title": "title",
            "content": "this is the content",
        }

        self.user = User.objects.create_user(username='admin', password='admin55')
        
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.data = {
            "username": "user",
            "password": "Index11#",
            "confirm_password": "Index11#"
        }

        self.post = BlogPost.objects.create(**self.valid_post_data, author=self.user)

        return super().setUp()
  
    def tearDown(self):
        return super().tearDown()
  

class TestViews(TestSetup):
    """
    Test creating using profile with valid data
    """

    def test_userprofile_with_data(self):
        resp = self.client.post(self.user_profile, self.data)
        self.assertEqual(resp.status_code, 201)
  
    def test_create_post_with_valid_data(self):
        response = self.client.post(self.post_create_url, self.valid_post_data)
        self.assertEqual(response.status_code, 201)
  
    def test_post_detail_with_valid_pk(self):
        response = self.client.get(reverse('post-detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        # Check that the response data matches the created post data
        self.assertEqual(response.data['title'], self.valid_post_data['title'])
        self.assertEqual(response.data['content'], self.valid_post_data['content'])

    def test_post_detail_with_invalid_pk(self):
        response = self.client.get(reverse('post-detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_post_update_with_valid_data(self):
        update_data = {
            "title": "new title",
            "content": "new content"
        }
        post_update_url = reverse(self.post_update_url_template, args=[self.post.pk])

        response = self.client.put(post_update_url, update_data)
        self.assertEqual(response.status_code, 200)

    def test_post_update_with_invalid_pk(self):
        invalid_pk = 9999

        post_update_url = reverse(self.post_update_url_template, args=[invalid_pk])

        response = self.client.put(post_update_url, {"title": "New Title", "content": "New Content"})
        self.assertEqual(response.status_code, 404)

    def test_delete_post_with_valid_pk(self):
        post_delete_url = reverse(self.post_delete_url_template, kwargs={'pk': self.post.pk})
        response = self.client.delete(post_delete_url)
        self.assertEqual(response.status_code, 204)
        # Check if post has been deleted
        post_exists = BlogPost.objects.filter(pk=self.post.pk).exists()
        self.assertFalse(post_exists)


    def test_get_posts_by_author(self):
        # Create a second user (author) and associate a post with it
        author = User.objects.create_user(username='author', password='author55')
        self.post.author = author  # Link the post to the author
        self.post.save()  # Save the changes


        response = self.client.get(reverse('posts-by-author', args=[author.pk]))  # Call the new endpoint
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Expecting one post in this author's posts
        self.assertEqual(response.data[0]['title'], self.post.title)


    def test_get_posts_by_category(self):
        # Create a category and associate a post with it
        category = Category.objects.create(name='Test Category')
        self.post.category = category  # Link the post to the category
        self.post.save()  # Save the changes


        response = self.client.get(reverse('posts-by-category', args=[category.pk]))  # Call the new endpoint
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Expecting one post in this category
        self.assertEqual(response.data[0]['title'], self.post.title)


    def test_search_blog_posts_by_title(self):
        response = self.client.get(reverse('post-search'), {'search': 'title'})  # Replace 'title' with actual title
        self.assertEqual(response.status_code, 200)
        self.assertIn('title', [post['title'] for post in response.data])  # Check if the post with the title is included


    def test_search_blog_posts_by_content(self):
        response = self.client.get(reverse('post-search'), {'search': 'content'})  # Replace 'content' with actual content
        self.assertEqual(response.status_code, 200)
        self.assertIn('this is the content', [post['content'] for post in response.data])  # Check if the content is included


    def test_search_blog_posts_by_tag(self):
        tag = Tag.objects.create(name='Django')
        self.post.tags.add(tag)
        
        response = self.client.get(reverse('post-search'), {'search': 'Django'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post.title, [post['title'] for post in response.data])  # Check if the post with the tag is included


    def test_search_blog_posts_by_author(self):
        response = self.client.get(reverse('post-search'), {'search': 'admin'})  # Assuming 'admin' is the username
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post.title, [post['title'] for post in response.data])  # Check if the post by admin is included

