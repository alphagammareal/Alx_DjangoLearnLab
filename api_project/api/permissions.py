from rest_framework.permissions import BasePermission

class IsTitleLongerThanFive(BasePermission):
    def has_object_permission(self, request, view, obj):
        return len(obj.title) > 5
