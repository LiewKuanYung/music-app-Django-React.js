from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        # all the fields here match room model
        fields = ('id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at')