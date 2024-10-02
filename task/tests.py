from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Ticket
from user.models import User

class TicketTests(APITestCase):

    def setUp(self):
        # Create a manager user
        self.manager = User.objects.create_user(username='manager', password='password', role='manager')
        self.client.login(username='manager', password='password')  # Log the manager in

    def test_create_ticket_as_manager(self):
        response = self.client.post(reverse('ticket-list'), {  # Ensure correct endpoint
            'task_type': 'task',
            'priority': 'high',
            'status': 'to_do',
            'title': 'Test Ticket',
            'description': 'This is a test ticket.'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_ticket_as_manager(self):
        ticket = Ticket.objects.create(
            task_type='task',
            priority='high',
            status='to_do',
            title='Test Ticket',
            description='This is a test ticket.',
            creator=self.manager
        )
        response = self.client.delete(reverse('ticket-detail', args=[ticket.number]))  # Use 'ticket-detail'
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_forbid_testers_in_progress(self):
        tester = User.objects.create_user(username='tester', password='password', role='tester')
        ticket = Ticket.objects.create(
            task_type='task',
            priority='high',
            status='to_do',
            title='Test Ticket',
            description='This is a test ticket.',
            creator=self.manager
        )
        response = self.client.patch(reverse('ticket-detail', args=[ticket.number]), {
            'status': 'in_progress',
            'assignee': tester.id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_ticket_status_transition(self):
        ticket = Ticket.objects.create(
            task_type='task',
            priority='high',
            status='to_do',
            title='Test Ticket',
            description='This is a test ticket.',
            creator=self.manager
        )
        response = self.client.patch(reverse('ticket-detail', args=[ticket.number]), {
            'status': 'done',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
