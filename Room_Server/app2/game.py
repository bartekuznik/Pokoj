from channels.generic.websocket import AsyncWebsocketConsumer
from .dtoObjects.Greeting import Greeting
from .dtoObjects.Move import Move
from .dtoObjects.UpdateTable import UpdateTable
from .dtoObjects.PokerGame import PokerGame
from .dtoObjects.SmallPlayer import SmallPlayer
import json
from django.db import connection
from .dtoObjects.Cards import MainCards
from .models import PlayerInGame, Room
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .serializers import *
from django.forms.models import model_to_dict
import asyncio
from asgiref.sync import async_to_sync
import os
import glob
from django.db import transaction
from django.db.utils import IntegrityError
from time import sleep


class GameConsumer(AsyncWebsocketConsumer):
    game = PokerGame(list())
    async def connect(self):
        await self.accept()
        # room
        self.chat_room = "game"
        # self.game.addWatcher()
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name)


    async def receive(self, text_data):
        print(text_data)
        data = json.loads(text_data)

        if data["type"] == "PlayerInfo":
            print("hejo")
            watcher = PlayerInGame(
                player_nick=data["player_nick"],
                card_1=None,
                card_2=None,
                tokens=data["tokens"],
                winPercentage=None
            )
            await reset_id(PlayerInGame)
            await save_model(watcher)

            self.game.addWatcher(
                SmallPlayer(
                    data["player_nick"],
                    None,
                    None,
                    0
                )

            )
            print(len(self.game.watchers), self.game.watchers, "HHHHHHHHHHHHHHHEEEEEEEEE")
            if len(self.game.watchers) == 2:
                print("LETSGO")
                if not self.game.isRunning:

                    A, B = self.game.startGame()
                    await decrease_player_money(A.nick,50)
                    await decrease_player_money(B.nick,100)
                    await update_player_card(A.nick,A.card1,A.card2)
                    await update_player_card(B.nick,B.card1,B.card2)
                    await increase_room_tokens(50)
                    await increase_room_tokens(100)
                    await nextPlayer(self.game.playerInMove)
                    await get_room_card(self.game)
                    await get_room_card(self.game)
                    await get_room_card(self.game)
                    await self.updateTable()

            elif len(self.game.watchers) == 1:
                roomData = await get_model("Room")
                playersData = await get_model("PlayerInGame")
                combinedData = UpdateTable(roomData, playersData)
                jsonData = json.dumps(combinedData.to_json())
                await self.send(jsonData)
            else:
                roomData = await get_model("Room")
                playersData = await get_model("PlayerInGame")
                combinedData = UpdateTable(roomData, playersData)
                jsonData = json.dumps(combinedData.to_json())
                await self.send(jsonData)

        if data["type"] == "Move":
            del data["type"]
            move = Move(**data)
            match (move.moveType):
                case "Bet":
                    self.game.bet(move)
                    await decrease_player_money(move.nick,move.amount)
                    await increase_room_tokens(move.amount)
                    self.game.nextPlayer()
                    await nextPlayer(self.game.playerInMove)
                    await self.updateTable()
                case "Call":
                    self.game.call(move)
                    await decrease_player_money(move.nick, move.amount)
                    await increase_room_tokens(move.amount)
                    self.game.nextPlayer()
                    await nextPlayer(self.game.playerInMove)
                    await self.updateTable()
                case "Fold":
                    self.game.fold(move)
                    await reset_player_cards(move.nick)
                    self.game.nextPlayer()
                    await nextPlayer(self.game.playerInMove)
                    await self.updateTable()
                case _:
                    ...
            print("MOREEEEEEEE")
            if self.game.playerInMove == "":
                if self.game.round ==4:
                    winner = self.game.getWinner()
                    print("WINNER",winner)
                    tokens = await get_room_tokens()
                    print(tokens,"CZASH")
                    await increase_player_tokens(winner,tokens)
                    await self.updateTable()
                    self.game.endGame()
                    await self.beginGame()

                else:
                    self.game.calculateBestHand()
                    await setPlayersWinrate(self.game.playersInGame)
                    await asyncio.sleep(1)
                    self.game.nextPlayer()
                    await nextPlayer(self.game.playerInMove)
                    await get_room_card(self.game)
                    await self.updateTable()

    async def beginGame(self):

        #TODO nie chce mi się neich ktoś zrobi zaczynainie 2giej partii




        print("dupa")
        # jsonMove = json.dumps(move.to_json(), indent=2)
        #
        # move_dict = move.to_json()
        # print(move_dict, type(move_dict))
        # # print(move.to_json())
        # await self.channel_layer.group_send(
        #     self.chat_room,
        #     {
        #         'type': 'move.message',
        #         'message': move_dict
        #     }
        # )
    async def updateTable(self):
        roomData = await get_model("Room")
        playersData = await get_model("PlayerInGame")
        combinedData = UpdateTable(roomData, playersData)
        jsonData = json.dumps(combinedData.to_json())
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'move.message',
                'message': jsonData
            }
        )

    async def endGame(self):
        winner = self.game.findWinner()
    async def move_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=message)

    async def handle_message(self, event):
        print(event)
        data = event['data']


        # add the new player to the watchers list
        self.game.addWatcher(data['player_nick'])

    def disconnect(self, close_code):
        # Remove the consumer from the group
        self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )

@sync_to_async()
def get_model(model):
    if model == "Room":
        room = Room.objects.filter(id=1).values().first()
        # print(room, type(room))
        return room
    elif model == "PlayerInGame":
        player_dicts = []
        for player in list(PlayerInGame.objects.values()):
            player_dict = player.copy()
            player_dict.pop("id")
            if 'card_1' in player_dict:
                new_card_1 = {'card': player_dict['card_1']}
                player_dict['card_1'] = new_card_1

                # Check and update 'card_2'
            if 'card_2' in player_dict:
                new_card_2 = {'card': player_dict['card_2']}
                player_dict['card_2'] = new_card_2
            player_dicts.append(player_dict)
            # print(("hhhhhhhhhhhhhhhhheeeeeee"),player_dict)
        # print(player_dicts, type(player_dicts))
        return player_dicts

@sync_to_async()
def get_room_tokens():
    room = Room.objects.get(id=1)
    tokens = room.tokensOnTable
    print(tokens,"TOOKENS")
    room.tokensOnTable = 0
    room.lastCall = 0
    room.save()
    return tokens
@sync_to_async()
def increase_player_tokens(nick,amount):
    player = PlayerInGame.objects.get(player_nick=nick)
    player.tokens += amount
    player.save()
@sync_to_async()
def get_room_card(pokerGame: PokerGame):
    room = Room.objects.get(id=1)
    cards = pokerGame.getNextTableCard()
    new_list = []
    for card in cards:
        new_item = {"card": card}
        new_list.append(new_item)
    room.cardsOnTable = new_list
    room.save()
@sync_to_async()
def setPlayersWinrate(players:list[SmallPlayer]):
    for player in players:
        playerInGame = PlayerInGame.objects.get(player_nick=player.nick)
        playerInGame.winPercentage = player.winPercentage
        playerInGame.save()

@sync_to_async()
def reset_player_cards(nick):
    player = PlayerInGame.objects.get(player_nick=nick)
    player.card_1 = None
    player.card_2 = None
    player.save()

@sync_to_async()
def nextPlayer(nick):
    room = Room.objects.get(id=1)
    room.nextPlayer = nick
    room.save()
@sync_to_async()
def increase_room_tokens(amount):
    room = Room.objects.get(id=1)
    room.tokensOnTable += amount
    room.lastCall = amount
    room.save()

@sync_to_async()
def decrease_player_money(nick,amount):
    player = PlayerInGame.objects.get(player_nick=nick)
    player.tokens -= amount
    player.save()
@sync_to_async()
def update_player_card(nick,card1,card2):
    player = PlayerInGame.objects.get(player_nick=nick)
    player.card_1 = card1
    player.card_2 = card2
    player.save()
@sync_to_async
def save_model(model):
    model.save()

@sync_to_async
def reset_id(model):
    #reset_id(PlayerInGame/Room)
    table_name = model._meta.db_table
    # print(table_name)
    with connection.cursor() as cursor:
        # cursor.execute(f"UPDATE {table_name} SET seq = 0 WHERE sqlite_sequence.name =  id;")
        # cursor.execute(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1")
        cursor.execute(f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table_name}'")

def toCardObject(card):
    return {
        "card": card
    }