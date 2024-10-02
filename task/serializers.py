from rest_framework import serializers
from .models import Ticket
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']

class TicketSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['number', 'task_type', 'priority', 'status', 'title', 'description', 'assignee', 'creator', 'blocking_tasks']
        read_only_fields = ['number', 'created_at', 'updated_at', 'creator']  # Creator is set automatically

    def validate(self, data):
        assignee = data.get('assignee')
        previous_status = data.get('previous_status')  # This should be provided during updates

        # Validate that assignee exists if provided
        if assignee is not None:
            if not User.objects.filter(id=assignee.id).exists():
                raise serializers.ValidationError("Assignee does not exist.")
        
            # Role-based restrictions
            if data['status'] in ['in_progress', 'code_review', 'dev_test'] and assignee.role == 'tester':
                raise serializers.ValidationError("A tester cannot be assigned to this task status.")
            
            if data['status'] == 'testing' and assignee.role == 'developer':
                raise serializers.ValidationError("A developer cannot be assigned to testing tasks.")

            if data['status'] == 'in_progress' and assignee is None:
                raise serializers.ValidationError("An assignee is required for 'in progress' tasks.")

        # Validate status transitions
        valid_transitions = {
            'to_do': ['in_progress', 'wontfix'],
            'in_progress': ['code_review', 'dev_test', 'done'],
            'code_review': ['dev_test', 'done'],
            'dev_test': ['testing', 'done'],
            'testing': ['done'],
            'done': [],  # No further transitions allowed
            'wontfix': []  # No further transitions allowed
        }

        if previous_status and data['status'] not in valid_transitions.get(previous_status, []):
            raise serializers.ValidationError(f"Cannot transition from {previous_status} to {data['status']}.")

        return data
