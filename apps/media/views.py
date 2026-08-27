from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.records.models import Record

from .models import Media
from .serializers import MediaSerializer
from .services import create_media, delete_media


class RecordMediaListCreateView(APIView):
	parser_classes = (MultiPartParser, FormParser)
	permission_classes = (IsAuthenticated,)

	def get(self, request, record_id):
		record = get_object_or_404(Record, pk=record_id)
		if record.user_id != request.user.id and not request.user.is_staff:
			return Response({'detail': 'You do not have permission to access this record.'}, status=status.HTTP_403_FORBIDDEN)
		serializer = MediaSerializer(record.media.all(), many=True, context={'request': request})
		return Response(serializer.data)

	def post(self, request, record_id):
		record = get_object_or_404(Record, pk=record_id)
		if record.user_id != request.user.id:
			return Response({'detail': 'Only the record creator can add media.'}, status=status.HTTP_403_FORBIDDEN)
		serializer = MediaSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		media = create_media(record=record, uploaded_file=serializer.validated_data['file'], media_type=serializer.validated_data['media_type'])
		return Response(MediaSerializer(media, context={'request': request}).data, status=status.HTTP_201_CREATED)


class MediaDeleteView(APIView):
	permission_classes = (IsAuthenticated,)

	def delete(self, request, pk):
		media = get_object_or_404(Media, pk=pk)
		if media.record.user_id != request.user.id and not request.user.is_staff:
			return Response({'detail': 'You do not have permission to delete this media.'}, status=status.HTTP_403_FORBIDDEN)
		delete_media(media)
		return Response(status=status.HTTP_204_NO_CONTENT)
