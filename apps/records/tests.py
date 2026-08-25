from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Record


class RecordModelTests(TestCase):
	def test_record_defaults_to_pending(self):
		user = get_user_model().objects.create_user(username='owner', password='pass12345')
		record = Record.objects.create(
			user=user,
			title='Broken road',
			description='The road is impassable after rainfall.',
			type=Record.RecordType.INTERVENTION,
		)

		self.assertEqual(record.status, Record.Status.PENDING)
		self.assertEqual(str(record), 'Broken road (Intervention)')
