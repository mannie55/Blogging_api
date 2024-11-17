



























































# class TestView(TestSetup):

#     def test_list_comments(self):
#         """Test that comments can be retrieved by post_id."""
#         response = self.client.get(reverse("comments-by-post", kwargs={"post_id": self.post.id}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]["content"], self.comment.content)

#     def test_create_comment_authenticated(self):
#         """Test that an authenticated user can create a comment."""
#         data = {
#             "content": "New comment",
#             "post": self.post.id
#         }
#         response = self.client.post(self.comment_list_url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Comment.objects.count(), 2)
#         self.assertEqual(response.data["author"], self.user.id)

#     def test_create_comment_unauthenticated(self):
#         """Test that an unauthenticated user cannot create a comment."""
#         self.client.credentials()  # Remove authentication
#         data = {
#             "content": "Another comment",
#             "post": self.post.id
#         }
#         response = self.client.post(self.comment_list_url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(Comment.objects.count(), 1)

#     def test_get_comment_detail(self):
#         """Test that a specific comment's detail can be retrieved."""
#         response = self.client.get(reverse(self.comment_detail_url_template, kwargs={"pk": self.comment.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["content"], self.comment.content)

#     def test_update_comment(self):
#         """Test that an authenticated user can update their own comment."""
#         data = {
#             "content": "Updated comment content"
#         }
#         response = self.client.patch(reverse(self.comment_detail_url_template, kwargs={"pk": self.comment.pk}), data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.comment.refresh_from_db()
#         self.assertEqual(self.comment.content, "Updated comment content")

#     def test_delete_comment(self):
#         """Test that an authenticated user can delete their own comment."""
#         response = self.client.delete(reverse(self.comment_detail_url_template, kwargs={"pk": self.comment.pk}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Comment.objects.count(), 0)





