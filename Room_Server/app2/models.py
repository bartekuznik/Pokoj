from django.db import models

# Create your models here.

class PlayerInGame(models.Model):
    player_id = models.PositiveIntegerField(unique=True,default=True)
    player_nick = models.TextField(max_length=200)
    is_win = models.BooleanField(default=False)
    card_1 = models.CharField(max_length=20)
    card_2 = models.CharField(max_length=20)

class Room(models.Model):
    card_1 = models.CharField(max_length=20)
    card_2 = models.CharField(max_length=20)
    card_3 = models.CharField(max_length=20)
    card_4 = models.CharField(max_length=20)
    card_5 = models.CharField(max_length=20)
    max_player_num = models.PositiveIntegerField(default=4)
    current_player_num = models.PositiveBigIntegerField(default=0)
    coins = models.PositiveIntegerField()
