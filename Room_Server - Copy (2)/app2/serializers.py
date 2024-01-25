from rest_framework import serializers
from .models import Room, PlayerInGame

class PlayerGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerInGame
        fields = [
            'player_nick'
            'card_1',
            'card_2',
            'tokens',
            'winPercentage'
        ]

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'cardsOnTable',
            'nextPlayer',
            'tokensOnTable',
            'lastCall'
        ]