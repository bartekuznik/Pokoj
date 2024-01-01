from channels.generic.websocket import AsyncWebsocketConsumer
from .dtoObjects.Greeting import Greeting
from .dtoObjects.Move import Move
import json
import asyncio
from asgiref.sync import async_to_sync


class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        await self.accept()
        self.chat_room = "game"
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name)
        await asyncio.sleep(0.5)
        greeting = Greeting("hello mello")
        jsonGreeting = json.dumps(greeting.to_json(), indent=2)
        print(f"connected and sent{jsonGreeting}\n\n\n\n\n")
        await self.send(text_data=jsonGreeting)

    async def receive(self, text_data):
        print(text_data)
        data = json.loads(text_data)

        move = Move(**data)

        jsonMove = json.dumps(move.to_json(), indent=2)

        move_dict = move.to_json()
        print(move_dict, type(move_dict))
        # print(move.to_json())
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'move.message',
                'message': move_dict
            }
        )

    async def move_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    def disconnect(self, close_code):
        # Remove the consumer from the group
        self.channel_layer.group_discard(
            self.move_group_name,
            self.channel_name
        )
