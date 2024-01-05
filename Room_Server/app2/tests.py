from django.test import TestCase
from .models import PlayerInGame, Room
import json


class CreateNewPlayer(TestCase):
    def test_user(self):
        newPlayer = Room(
            id=0,
            cardsOnTable=
            [
                {"card": "clubs_2"},
                {"card": "clubs_2"},
                {"card": "clubs_2"},
                {"card": "clubs_2"},
                {"card": "clubs_2"}
            ],

            nextPlayer="karol",
            tokensOnTable=50,
            lastCall=20
        )

        newPlayer.save()

    def test_rooms(self):
        newPlayer = PlayerInGame.objects.create(
            player_id=0,
            player_nick="karol",
            card_1="clubs_2",
            card_2="clubs_2",
            tokens=500,
        )
        newPlayer.save()
        self.assertTrue(
            hasattr(newPlayer, 'player_id')
        )
