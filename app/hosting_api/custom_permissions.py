from rest_framework.permissions import BasePermission


class CanCreateTempLinks(BasePermission):
    message = 'Creating temporary links is for users with such permission'

    def has_permission(self, request, view):
        if request.user:
            if request.user.account_plan.can_expire_links:
                return True
        return False
