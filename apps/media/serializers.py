from rest_framework import serializers

from .models import Media


class MediaSerializer(serializers.ModelSerializer):
	url = serializers.SerializerMethodField()

	class Meta:
		model = Media
		fields = ('id', 'record', 'file', 'url', 'media_type', 'created_at')
		read_only_fields = ('id', 'record', 'url', 'created_at')

	def get_url(self, obj):
		request = self.context.get('request')
		url = obj.file.url
		return request.build_absolute_uri(url) if request else url

	def validate(self, attrs):
		uploaded_file = attrs.get('file')
		media_type = attrs.get('media_type')
		extension = uploaded_file.name.rsplit('.', 1)[-1].lower() if uploaded_file and '.' in uploaded_file.name else ''
		image_extensions = {'jpg', 'jpeg', 'png', 'gif'}
		video_extensions = {'mp4', 'mov', 'webm'}

		if media_type == Media.MediaType.IMAGE and extension not in image_extensions:
			raise serializers.ValidationError({'file': 'Image uploads must be jpg, jpeg, png, or gif files.'})
		if media_type == Media.MediaType.VIDEO and extension not in video_extensions:
			raise serializers.ValidationError({'file': 'Video uploads must be mp4, mov, or webm files.'})
		return attrs
