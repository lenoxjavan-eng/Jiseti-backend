from django.core.validators import FileExtensionValidator
from django.db import models


class Media(models.Model):
	class MediaType(models.TextChoices):
		IMAGE = 'image', 'Image'
		VIDEO = 'video', 'Video'

	record = models.ForeignKey('records.Record', on_delete=models.CASCADE, related_name='media')
	file = models.FileField(
		upload_to='records/media/%Y/%m/%d/',
		validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'webm'])],
	)
	media_type = models.CharField(max_length=10, choices=MediaType.choices)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at',)
