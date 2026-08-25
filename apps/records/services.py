from .models import Record


def create_record(*, user, **validated_data):
	"""Create a record owned by the authenticated user."""
	return Record.objects.create(user=user, **validated_data)
