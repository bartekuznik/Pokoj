from django.db import models
# Create your models here.


class PlayerInGame(models.Model):
    # player_id = models.PositiveIntegerField(unique=True,default=True)
    player_nick = models.TextField(max_length=200)
    card_1 = models.CharField(max_length=20,null=True)
    card_2 = models.CharField(max_length=20,null=True)
    tokens = models.IntegerField(default=0)
    winPercentage = models.FloatField(null=True)


class Room(models.Model):
    cardsOnTable = models.JSONField()
    nextPlayer = models.CharField(max_length=200)
    tokensOnTable = models.PositiveIntegerField(default=0)
    lastCall = models.PositiveIntegerField(default=0)
    isFinished = models.BooleanField(default=False)
