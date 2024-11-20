from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.ReadOnlyField(source="assigned_to.username")

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "status",
            "assigned_to",
            "assigned_to_username",
            "date_created",
            "date_updated",
        ]
