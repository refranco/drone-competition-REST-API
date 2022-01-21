from rest_framework import permissions

class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			# The method is a safe method
			return True
		else:
			# the method isn't a safe method
			# only owner are granted permision for safe methods
			return obj.owner == request.user

	    