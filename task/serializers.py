from rest_framework import serializers
from .models import Ticket
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']

class TicketSerializer(serializers.ModelSerializer):
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)

    class Meta:
        model = Ticket
        fields = ['number', 'task_type', 'priority', 'status', 'title', 'description', 'assignee', 'creator', 'blocking_tasks']
        read_only_fields = ['number', 'created_at', 'updated_at', 'creator']  # Creator is set automatically

    def validate(self, data):
        assignee = data.get('assignee')
        previous_status = data.get('previous_status')  # This should be provided during updates

        # Validate that assignee exists if provided
        if assignee is not None:
            # Role-based restrictions
            if data['status'] in ['in_progress', 'code_review', 'dev_test'] and assignee.role == 'tester':
                raise serializers.ValidationError("A tester cannot be assigned to this task status.")
            
            if data['status'] == 'testing' and assignee.role == 'developer':
                raise serializers.ValidationError("A developer cannot be assigned to testing tasks.")

            if data['status'] == 'in_progress' and assignee is None:
                raise serializers.ValidationError("An assignee is required for 'in progress' tasks.")

        # Validate status transitions
        valid_transitions = {
            'todo': ['todo', 'wontfix', 'in_progress'],
            'in_progress': ['todo', 'wontfix', 'code_review',],
            'code_review': ['todo', 'wontfix', 'dev_test'],
            'dev_test': ['todo', 'wontfix', 'testing'],
            'testing': ['todo', 'wontfix', 'done'],
            'done': ['todo', 'done'],
            'wontfix': ['todo','wontfix'],
        }

        if previous_status and data['status'] not in valid_transitions.get(previous_status, []):
            raise serializers.ValidationError(f"Cannot transition from {previous_status} to {data['status']}.")

        return data

    def create(self, validated_data):
        # Automatically set the creator to the current user when creating a ticket
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        previous_status = instance.status  # Capture previous status for validation
        validated_data['previous_status'] = previous_status  # Add previous status for validation
        return super().update(instance, validated_data)
