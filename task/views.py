# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.exceptions import PermissionDenied
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters
# from .models import Ticket
# from .serializers import TicketSerializer
# from user.models import User  # Make sure to import the User model
# from user.permissions import CanEditTicket, CanDeleteTicket, IsManager


# class TicketCreateView(generics.ListCreateAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#     permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access tickets
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     search_fields = ['title', 'description', 'number']
#     filterset_fields = ['task_type', 'status', 'creator', 'assignee']

#     def perform_create(self, serializer):
#         # Automatically set the creator to the current user
#         serializer.save(creator=self.request.user)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class TicketRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#     permission_classes = [permissions.IsAuthenticated, CanEditTicket]
#     lookup_field = 'number'  # Use 'number' as the lookup field instead of 'pk'

#     def perform_update(self, serializer):
#         serializer.save()

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         previous_status = instance.status
#         new_status = request.data.get('status')

#         # Ensure status transition is valid
#         if not self.is_valid_status_transition(previous_status, new_status):
#             return Response({"detail": f"Cannot transition from {previous_status} to {new_status}."}, status=status.HTTP_400_BAD_REQUEST)

#         # Fetch assignee as a User object
#         assignee_id = request.data.get('assignee', instance.assignee.id if instance.assignee else None)
#         assignee = None
#         if assignee_id:
#             try:
#                 assignee = User.objects.get(id=assignee_id)
#             except User.DoesNotExist:
#                 return Response({"detail": "Assignee not found."}, status=status.HTTP_400_BAD_REQUEST)

#         # Ensure role-specific constraints are valid
#         if not self.is_valid_role_assignment(new_status, assignee):
#             return Response({"detail": "Role-specific constraints violated."}, status=status.HTTP_400_BAD_REQUEST)

#         # Proceed with the update
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     def is_valid_status_transition(self, previous_status, new_status):
#         valid_transitions = {
#             'todo': ['todo', 'wontfix', 'in_progress'],
#             'in_progress': ['in_progress', 'code_review'],
#             'code_review': ['code_review', 'dev_test'],
#             'dev_test': ['dev_test', 'testing'],
#             'testing': ['testing', 'done'],
#             'done': ['done'],
#             'wontfix': ['wontfix'],
#         }
#         return new_status in valid_transitions.get(previous_status, [])

#     def is_valid_role_assignment(self, new_status, assignee):
#         if new_status in ['in_progress', 'code_review', 'dev_test'] and assignee and assignee.role == 'tester':
#             return False
#         if new_status == 'testing' and assignee and assignee.role == 'developer':
#             return False
#         if new_status == 'in_progress' and not assignee:
#             return False  # Assignee is required for 'in progress'
#         return True

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()

#         # Check if the user has permission to delete the ticket
#         if not CanDeleteTicket().has_permission(request, self):
#             return Response({"detail": "You do not have permission to delete this ticket."}, status=status.HTTP_403_FORBIDDEN)

#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class TicketListView(APIView):
#     permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access this view
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     search_fields = ['title', 'description', 'number']
#     filterset_fields = ['task_type', 'status', 'creator', 'assignee']

#     def get(self, request):
#         # Apply filtering and searching to the queryset
#         tickets = Ticket.objects.all()

#         # Filters
#         task_type = request.query_params.get('task_type')
#         status = request.query_params.get('status')
#         creator = request.query_params.get('creator')
#         assignee = request.query_params.get('assignee')

#         if task_type:
#             tickets = tickets.filter(task_type=task_type)
#         if status:
#             tickets = tickets.filter(status=status)
#         if creator:
#             tickets = tickets.filter(creator__id=creator)
#         if assignee:
#             tickets = tickets.filter(assignee__id=assignee)

#         # Serialize the data
#         serializer = TicketSerializer(tickets, many=True)

#         # Return the serialized data as a JSON response
#         return Response(serializer.data)





from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Ticket
from .serializers import TicketSerializer
from user.models import User  # Make sure to import the User model
from user.permissions import CanEditTicket, CanDeleteTicket

class TicketCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access tickets
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description', 'number']
    filterset_fields = ['task_type', 'status', 'creator', 'assignee']

    def perform_create(self, serializer):
        # Automatically set the creator to the current user
        serializer.save(creator=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TicketRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, CanEditTicket]
    lookup_field = 'number'  # Use 'number' as the lookup field instead of 'pk'

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        previous_status = instance.status
        new_status = request.data.get('status')

        # Ensure status transition is valid
        if not self.is_valid_status_transition(previous_status, new_status):
            return Response({"detail": f"Cannot transition from {previous_status} to {new_status}."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch assignee as a User object
        assignee_id = request.data.get('assignee', instance.assignee.id if instance.assignee else None)
        assignee = None
        if assignee_id:
            try:
                assignee = User.objects.get(id=assignee_id)
            except User.DoesNotExist:
                return Response({"detail": "Assignee not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure role-specific constraints are valid
        if not self.is_valid_role_assignment(new_status, assignee):
            return Response({"detail": "Role-specific constraints violated."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with the update
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def is_valid_status_transition(self, previous_status, new_status):
        valid_transitions = {
            'todo': ['todo', 'wontfix', 'in_progress'],
            'in_progress': ['wontfix', 'code_review',],
            'code_review': ['wontfix', 'dev_test'],
            'dev_test': ['wontfix', 'testing'],
            'testing': ['wontfix', 'done'],
            'done': ['done'],
            'wontfix': ['wontfix'],
        }
        return new_status in valid_transitions.get(previous_status, [])

    def is_valid_role_assignment(self, new_status, assignee):
        if new_status in ['in_progress', 'code_review', 'dev_test'] and assignee and assignee.role == 'tester':
            return False
        if new_status == 'testing' and assignee and assignee.role == 'developer':
            return False
        if new_status == 'in_progress' and not assignee:
            return False  # Assignee is required for 'in progress'
        return True

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the user has permission to delete the ticket
        if not CanDeleteTicket().has_permission(request, self):
            return Response({"detail": "You do not have permission to delete this ticket."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TicketListView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access this view
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description', 'number']
    filterset_fields = ['task_type', 'status', 'creator', 'assignee']

    def get(self, request):
        # Apply filtering and searching to the queryset
        tickets = Ticket.objects.all()

        # Filters
        task_type = request.query_params.get('task_type')
        status = request.query_params.get('status')
        creator = request.query_params.get('creator')
        assignee = request.query_params.get('assignee')

        if task_type:
            tickets = tickets.filter(task_type=task_type)
        if status:
            tickets = tickets.filter(status=status)
        if creator:
            tickets = tickets.filter(creator__id=creator)
        if assignee:
            tickets = tickets.filter(assignee__id=assignee)

        # Serialize the data
        serializer = TicketSerializer(tickets, many=True)

        # Return the serialized data as a JSON response
        return Response(serializer.data)
