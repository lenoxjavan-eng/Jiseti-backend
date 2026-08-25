from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Record
from .serializers import RecordSerializer


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


class RecordSerializerTests(TestCase):
	def test_rejects_incomplete_location(self):
		serializer = RecordSerializer(data={
			'title': 'Polluted river',
			'description': 'Waste is being discharged into the river.',
			'type': Record.RecordType.RED_FLAG,
			'latitude': '-1.286389',
		})

		self.assertFalse(serializer.is_valid())
		self.assertIn('non_field_errors', serializer.errors)

	def test_rejects_out_of_range_coordinates(self):
		serializer = RecordSerializer(data={
			'title': 'Polluted river',
			'description': 'Waste is being discharged into the river.',
			'type': Record.RecordType.RED_FLAG,
			'latitude': '91.000000',
			'longitude': '36.821946',
		})

		self.assertFalse(serializer.is_valid())
		self.assertIn('latitude', serializer.errors)
