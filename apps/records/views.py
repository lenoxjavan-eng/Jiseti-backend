from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RecordSerializer
from .services import create_record, update_record
from .models import Record
from .permissions import IsOwnerOrAdmin, IsPendingRecord


class RecordListCreateView(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		queryset = request.user.records.all()
		if request.user.is_staff:
			from .models import Record
			queryset = Record.objects.all()
		return Response(RecordSerializer(queryset, many=True, context={'request': request}).data)

	def post(self, request):
		serializer = RecordSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		record = create_record(user=request.user, **serializer.validated_data)
		return Response(RecordSerializer(record, context={'request': request}).data, status=status.HTTP_201_CREATED)


class RecordDetailView(APIView):
	permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

	def get_object(self, pk):
		record = get_object_or_404(Record, pk=pk)
		self.check_object_permissions(self.request, record)
		return record

	def get(self, request, pk):
		record = self.get_object(pk)
		return Response(RecordSerializer(record, context={'request': request}).data)

	def put(self, request, pk):
		return self._update(request, pk, partial=False)

	def patch(self, request, pk):
		return self._update(request, pk, partial=True)

	def _update(self, request, pk, *, partial):
		record = self.get_object(pk)
		self.check_object_permissions(request, record)
		if not IsPendingRecord().has_object_permission(request, self, record):
			return Response({'detail': IsPendingRecord.message}, status=status.HTTP_403_FORBIDDEN)
		serializer = RecordSerializer(record, data=request.data, partial=partial, context={'request': request})
		serializer.is_valid(raise_exception=True)
		record = update_record(record=record, **serializer.validated_data)
		return Response(RecordSerializer(record, context={'request': request}).data)
