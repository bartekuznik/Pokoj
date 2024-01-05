from channels.generic.websocket import AsyncWebsocketConsumer
from .dtoObjects.Greeting import Greeting
from .dtoObjects.Move import Move
from .dtoObjects.UpdateTable import UpdateTable
from .dtoObjects.PokerGame import PokerGame
import json
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


class GameConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.game = PokerGame(list())
    async def connect(self):
        await self.accept()
        # room
        self.chat_room = "game"
        # self.game.addWatcher()
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name)

        # roomData = await sync_to_async(Room.objects.first)()
        #
        # roomData = model_to_dict(roomData)
        # # roomData = await database_sync_to_async(Room.objects.values().filter(id=1).first())()
        # playersData = await database_sync_to_async(list)(PlayerInGame.objects.all().values())
        # combinedData = UpdateTable(roomData, playersData)
        # jsonData = json.dumps(combinedData.to_json())
        # # jsonPlayersData = json.dumps({'Room:':playersData})
        # # await self.channel_layer.group_send(
        # #     self.channel_name,
        # #     {
        # #         'type': 'move.message',
        # #         'message': jsonTableData
        # #     }
        # # )
        # await self.send(jsonData)


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
            await save_model(watcher)

            self.game.addWatcher(watcher)
            if len(self.game.watchers) > 2:
                self.game.start_game()
            elif len(self.game.watchers) == 1:
                roomData = await get_model("Room")
                print("majonez",roomData, type(roomData))
                playersData = await get_model("PlayerInGame")
                print("majonez2",playersData, type(playersData))
                combinedData = UpdateTable(roomData, playersData)
                jsonData = json.dumps(combinedData.to_json())
                print("\n\n\n\n\n",jsonData)
                await self.send(jsonData)
            else:
                roomData = await get_model(Room)
                playersData = await get_model(PlayerInGame)
                print("majonez3", playersData, type(playersData))
                print("majonez4", roomData, type(roomData))
                combinedData = UpdateTable(roomData, playersData)
                jsonData = json.dumps(combinedData.to_json())
                await self.send(jsonData)
                print("\n\n\n\n\n222222", jsonData)




        if data["type"] == "Move":
            del data["type"]
            move = Move(**data)
            self.game.move(move)
            to_Delete = Room.objects.get(id=1)
            to_Delete.delete()
            updateRoom = Room(
                cardsOnTable=self.game.cardsOnTable,
                nextPlayer=self.game.playerInMove,
                tokensOnTable=self.game.tokensOnTable,
                lastCall=self.game.lastCall
            )
            updateRoom.save()
            jsonData = json.dumps()
        if data["type"] == "Ping":
            pinger = {"type": "Ping"}
            await self.send(json.dumps(pinger))
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
    def start_game(self):
        ...


    async def move_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


    def disconnect(self, close_code):
        # Remove the consumer from the group
        self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )
@sync_to_async()
def get_model(model, player_id=1):
    if model == "Room":
        room = Room.objects.filter(id=1).values().first()
        print(room, type(room))
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
            print(("hhhhhhhhhhhhhhhhheeeeeee"),player_dict)
        print(player_dicts, type(player_dicts))
        return player_dicts
        print(player, type(player))
        return player
@sync_to_async
def save_model(model):
    try:
        with transaction.atomic():
            model.save()
    except IntegrityError:
        pass
