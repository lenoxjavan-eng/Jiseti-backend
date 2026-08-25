from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
	"""Allow an owner to access a record and staff users to manage all records."""

	def has_object_permission(self, request, view, obj):
		return bool(request.user and request.user.is_staff) or obj.user_id == request.user.id


class IsPendingRecord(BasePermission):
	"""Only pending records may be edited or deleted by their owner."""

	message = 'Only pending records can be modified or deleted.'

	def has_object_permission(self, request, view, obj):
		return obj.status == obj.Status.PENDING
