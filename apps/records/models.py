from django.conf import settings
from django.db import models


class Record(models.Model):
	class RecordType(models.TextChoices):
		RED_FLAG = 'red-flag', 'Red flag'
		INTERVENTION = 'intervention', 'Intervention'

	class Status(models.TextChoices):
		PENDING = 'pending', 'Pending'
		UNDER_INVESTIGATION = 'under-investigation', 'Under investigation'
		REJECTED = 'rejected', 'Rejected'
		RESOLVED = 'resolved', 'Resolved'

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='records')
	title = models.CharField(max_length=255)
	description = models.TextField()
	type = models.CharField(max_length=20, choices=RecordType.choices)
	status = models.CharField(max_length=24, choices=Status.choices, default=Status.PENDING)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return f'{self.title} ({self.get_type_display()})'
