from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import BlogPost

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

    self.data={
      "username":"user",
      "password":"Index11#",
      "confirm_password":"Index11#"
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
    resp = self.client.post(self.user_profile,self.data)
    self.assertEqual(resp.status_code, 201)
  
  def test_create_post_with_valid_data(self):
    response = self.client.post(self.post_create_url, self.valid_post_data)
    self.assertEqual(response.status_code, 201)
  
  
  def test_post_detail_with_valid_uid(self):
    response = self.client.get(reverse('post-detail', args=[self.post.uid]))
    self.assertEqual(response.status_code, 200)
    #check that the response data matches the created post data
    self.assertEqual(response.data['title'], self.valid_post_data['title'])
    self.assertEqual(response.data['content'], self.valid_post_data['content'])


  def test_post_detail_with_invalid_uid(self):
    response = self.client.get(reverse('post-detail', args=["d15e5cbe-056c-43d8-87c0-31afe21e3666"]))
    self.assertEqual(response.status_code, 404)

  def test_post_update_with_valid_data(self):
    update_data = {
      "title":"new title",
      "content":"new content"
    }
    post_update_url = reverse(self.post_update_url_template, args=[self.post.uid])

    response = self.client.put(post_update_url, update_data)
    self.assertEqual(response.status_code, 200)

  def test_post_update_with_invalid_uid(self):

    invalid_uid = '12345678-1234-1234-1234-123456789abc'

    post_update_url = reverse(self.post_update_url_template, args=[invalid_uid])

    response = self.client.put(post_update_url, {"title": "New Title", "content": "New Content"})
    self.assertEqual(response.status_code, 404)

  def test_delete_post_with_valid_uid(self):
    post_delete_url = reverse(self.post_delete_url_template, kwargs={'uid': str(self.post.uid)})
    response = self.client.delete(post_delete_url)
    self.assertEqual(response.status_code, 204)
    # check if post has been deleted

    post_exists = BlogPost.objects.filter(uid=self.post.uid).exists()
    self.assertFalse(post_exists)