import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.records.models import Record

from .models import Media


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class MediaApiTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.record = Record.objects.create(latitude='6.524379', longitude='3.379206')
		self.list_url = f'/api/records/{self.record.pk}/media/'

	def test_upload_and_list_image(self):
		response = self.client.post(
			self.list_url,
			{
				'file': SimpleUploadedFile('evidence.jpg', b'image data', content_type='image/jpeg'),
				'media_type': 'image',
			},
			format='multipart',
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['media_type'], 'image')
		self.assertTrue(response.data['url'].startswith('http'))
		self.assertEqual(self.client.get(self.list_url).data[0]['id'], response.data['id'])

	def test_upload_and_delete_video(self):
		response = self.client.post(
			self.list_url,
			{
				'file': SimpleUploadedFile('clip.mp4', b'video data', content_type='video/mp4'),
				'media_type': 'video',
			},
			format='multipart',
		)

		delete_response = self.client.delete(f"/api/media/{response.data['id']}/")

		self.assertEqual(delete_response.status_code, 204)
		self.assertFalse(Media.objects.filter(pk=response.data['id']).exists())

	def test_image_type_rejects_video_extension(self):
		response = self.client.post(
			self.list_url,
			{
				'file': SimpleUploadedFile('clip.mp4', b'video data', content_type='video/mp4'),
				'media_type': 'image',
			},
			format='multipart',
		)

		self.assertEqual(response.status_code, 400)
		self.assertIn('file', response.data)
