from django.urls import path
from .views import TicketCreateView, TicketRetrieveUpdateDestroyView, TicketListView

urlpatterns = [
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:number>/', TicketRetrieveUpdateDestroyView.as_view(), name='ticket-detail'),
    path('tickets/create/', TicketCreateView.as_view(), name='ticket-create'),
]
