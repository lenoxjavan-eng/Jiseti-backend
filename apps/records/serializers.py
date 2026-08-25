from rest_framework import serializers

from .models import Record


class RecordSerializer(serializers.ModelSerializer):
	user_id = serializers.IntegerField(source='user.id', read_only=True)

	class Meta:
		model = Record
		fields = (
			'id', 'user_id', 'title', 'description', 'type', 'status', 'latitude',
			'longitude', 'created_at', 'updated_at',
		)
		read_only_fields = ('id', 'user_id', 'status', 'created_at', 'updated_at')
