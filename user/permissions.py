from .models import User
from wallet.models import Wallet
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == User.ROLE.ADMIN)

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == User.ROLE.MANAGER)

class IsSupport(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == User.ROLE.SUPPORT)

class IsSufficient(BasePermission):
    def has_permission(self, request, view):
        wallet = Wallet.objects.filter(user=request.user).first()
        balance = wallet.balance
        if balance <= 0:
            return bool(wallet and wallet.balance >= request.data.get("amount", 0))


class IsSupportorIsAdminorIsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.role in {User.ROLE.MANAGER, User.ROLE.SUPPORT, User.ROLE.ADMIN})
