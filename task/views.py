from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Ticket
from .serializers import TicketSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from user.permissions import CanEditTicket, CanDeleteTicket, IsManager

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access tickets
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description', 'number']
    filterset_fields = ['task_type', 'status', 'creator', 'assignee']

    def perform_create(self, serializer):
        # Automatically set the creator to the current user
        serializer.save(creator=self.request.user)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the user is allowed to update the ticket
        if not CanEditTicket().has_permission(request, self):
            return Response({"detail": "You do not have permission to update this ticket."}, status=status.HTTP_403_FORBIDDEN)

        # Validate status transitions
        previous_status = instance.status
        new_status = request.data.get('status')

        # Status transition logic
        valid_transitions = {
            'to_do': ['to_do', 'wontfix', 'in_progress'],
            'in_progress': ['in_progress', 'code_review'],
            'code_review': ['code_review', 'dev_test'],
            'dev_test': ['dev_test', 'testing'],
            'testing': ['testing', 'done'],
            'done': ['done'],
            'wontfix': ['wontfix'],
        }

        if new_status not in valid_transitions[previous_status]:
            return Response({"detail": f"Cannot transition from {previous_status} to {new_status}."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate role-specific constraints
        assignee = request.data.get('assignee', instance.assignee)
        if new_status in ['in_progress', 'code_review', 'dev_test'] and assignee and assignee.role == 'tester':
            return Response({"detail": "Tester cannot be assigned to this task status."}, status=status.HTTP_400_BAD_REQUEST)

        if new_status == 'testing' and assignee and assignee.role == 'developer':
            return Response({"detail": "Developer cannot be assigned to testing tasks."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate if assignee is required
        if new_status == 'in_progress' and not assignee:
            return Response({"detail": "Assignee is required for 'in progress' tasks."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with the update if all validations pass
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the user has permission to delete the ticket
        if not CanDeleteTicket().has_permission(request, self):
            return Response({"detail": "You do not have permission to delete this ticket."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = super().get_queryset()
        creator = self.request.query_params.get('creator', None)
        if creator:
            queryset = queryset.filter(creator__id=creator)
        return queryset
