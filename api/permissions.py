from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.cart_user==request.user

class IsOwnerOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.order_user==request.user