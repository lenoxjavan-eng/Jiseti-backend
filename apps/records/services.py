from .models import Record


def create_record(*, user, **validated_data):
	"""Create a record owned by the authenticated user."""
	return Record.objects.create(user=user, **validated_data)


def update_record(*, record, **validated_data):
	for field, value in validated_data.items():
		setattr(record, field, value)
	record.save()
	return record


def delete_record(*, record):
	record.delete()


def update_record_status(*, record, status):
	record.status = status
	record.save(update_fields=('status', 'updated_at'))
	return record
