from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'


class IsTeamLead(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teamlead'


class IsDeveloper(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'developer'


class IsTester(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'tester'


class CanEditTicket(BasePermission):
    def has_permission(self, request, view):
        # Allow editing if user is the creator of the ticket or a manager
        ticket = view.get_object() if hasattr(view, 'get_object') else None
        return request.user.is_authenticated and (request.user == ticket.creator or request.user.role == 'manager')

class CanDeleteTicket(BasePermission):
    def has_permission(self, request, view):
        # Allow deletion if user is a manager
        return request.user.is_authenticated and request.user.role == 'manager'
