from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
	"""Allow an owner to access a record and staff users to manage all records."""

	def has_object_permission(self, request, view, obj):
		return bool(request.user and request.user.is_staff) or obj.user_id == request.user.id
