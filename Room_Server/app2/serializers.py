from rest_framework import serializers
from .models import Room, PlayerInGame

class PlayerGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerInGame
        fields = [
            'player_id',
            'is_win',
            'card_1',
            'card_2',
        ]

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'card_1',
            'card_2',
            'card_3',
            'card_4',
            'card_5',
            'max_player_num',
            'current_player_num',
            'coins'
        ]