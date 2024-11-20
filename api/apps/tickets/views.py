from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Ticket
from .serializers import TicketSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all().order_by("-date_created")
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["priority", "status", "assigned_to"]
    search_fields = ["title", "description"]
    ordering_fields = ["date_created", "priority"]
