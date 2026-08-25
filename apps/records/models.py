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

	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at',)
