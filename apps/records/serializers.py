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

	def validate(self, attrs):
		latitude = attrs.get('latitude', getattr(self.instance, 'latitude', None))
		longitude = attrs.get('longitude', getattr(self.instance, 'longitude', None))

		if (latitude is None) != (longitude is None):
			raise serializers.ValidationError('Latitude and longitude must be supplied together.')
		if latitude is not None and not -90 <= latitude <= 90:
			raise serializers.ValidationError({'latitude': 'Latitude must be between -90 and 90.'})
		if longitude is not None and not -180 <= longitude <= 180:
			raise serializers.ValidationError({'longitude': 'Longitude must be between -180 and 180.'})
		return attrs
