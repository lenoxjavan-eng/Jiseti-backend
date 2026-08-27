from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Record
from .serializers import RecordSerializer


class RecordModelTests(TestCase):
	def test_record_defaults_to_pending(self):
		user = get_user_model().objects.create_user(email='owner@example.com', password='pass12345')
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


class RecordApiTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(email='owner@example.com', password='pass12345')
		self.other_user = get_user_model().objects.create_user(email='other@example.com', password='pass12345')
		self.client.force_authenticate(self.user)
		self.payload = {
			'title': 'Damaged bridge',
			'description': 'The bridge railing is damaged.',
			'type': Record.RecordType.RED_FLAG,
			'latitude': '-1.286389',
			'longitude': '36.821946',
		}

	def test_owner_can_create_and_list_records(self):
		create_response = self.client.post('/api/records/', self.payload, format='json')
		list_response = self.client.get('/api/records/my-records/')

		self.assertEqual(create_response.status_code, 201)
		self.assertEqual(create_response.data['status'], Record.Status.PENDING)
		self.assertEqual(list_response.status_code, 200)
		self.assertEqual(len(list_response.data), 1)

	def test_authenticated_users_can_list_all_records(self):
		Record.objects.create(user=self.other_user, **self.payload)

		response = self.client.get('/api/records/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 1)

	def test_staff_cannot_mutate_another_users_record(self):
		admin = get_user_model().objects.create_user(email='admin@example.com', password='pass12345', is_staff=True)
		record = Record.objects.create(user=self.user, **self.payload)
		self.client.force_authenticate(admin)

		response = self.client.patch(f'/api/records/{record.pk}/', {'title': 'Changed'}, format='json')

		self.assertEqual(response.status_code, 403)

	def test_owner_can_update_pending_record_location(self):
		record = Record.objects.create(user=self.user, **self.payload)

		response = self.client.patch(
			f'/api/records/{record.pk}/location/',
			{'latitude': '-1.300000', 'longitude': '36.900000'},
			format='json',
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['latitude'], '-1.300000')

	def test_owner_cannot_mutate_non_pending_record(self):
		record = Record.objects.create(user=self.user, status=Record.Status.RESOLVED, **self.payload)

		response = self.client.patch(f'/api/records/{record.pk}/', {'title': 'Changed'}, format='json')

		self.assertEqual(response.status_code, 403)
		record.refresh_from_db()
		self.assertEqual(record.title, self.payload['title'])

	def test_other_user_cannot_view_record(self):
		record = Record.objects.create(user=self.user, **self.payload)
		self.client.force_authenticate(self.other_user)

		response = self.client.get(f'/api/records/{record.pk}/')

		self.assertEqual(response.status_code, 403)

	def test_only_staff_can_update_record_status(self):
		record = Record.objects.create(user=self.user, **self.payload)
		response = self.client.patch(
			f'/api/admin/records/{record.pk}/status/',
			{'status': Record.Status.RESOLVED},
			format='json',
		)

		self.assertEqual(response.status_code, 403)
		record.refresh_from_db()
		self.assertEqual(record.status, Record.Status.PENDING)

	def test_staff_can_update_record_status(self):
		admin = get_user_model().objects.create_user(email='admin@example.com', password='pass12345', is_staff=True)
		record = Record.objects.create(user=self.user, **self.payload)
		self.client.force_authenticate(admin)

		response = self.client.patch(
			f'/api/admin/records/{record.pk}/status/',
			{'status': Record.Status.UNDER_INVESTIGATION},
			format='json',
		)

		self.assertEqual(response.status_code, 200)
		record.refresh_from_db()
		self.assertEqual(record.status, Record.Status.UNDER_INVESTIGATION)

	def test_status_update_rejects_unknown_status(self):
		admin = get_user_model().objects.create_user(email='admin@example.com', password='pass12345', is_staff=True)
		record = Record.objects.create(user=self.user, **self.payload)
		self.client.force_authenticate(admin)

		response = self.client.patch(
			f'/api/admin/records/{record.pk}/status/',
			{'status': 'closed'},
			format='json',
		)

		self.assertEqual(response.status_code, 400)
