import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
class GameConsumer(AsyncWebsocketConsumer):
    # async def websocket_connect(self, message):
    #
    #     await self.accept({
    #         'type': 'websocket.accept'
    #     })
    #     await self.send(text_data=json.dumps({
    #         'type': 'connection_established',
    #         'message': 'You are now connected'
    #     }))

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )

        await self.accept()
        await self.send("hello")
    # async def connect(self):
    #     # self.room_group_name = 'room 1'
    #     # async_to_sync(self.channel_layer.group_add)(
    #     #     self.room_group_name,
    #     #     self.channel_name
    #     # )
    #     await self.channel_layer.group_add()
    #     await self.accept()




    # async def websocket_receive(self, message):
    #     print('recevied message:', message)
    #     recevied_message = json.loads(message)
    #     msg = recevied_message.get('message')
    #     # sent_by_id = recevied_message.get('sent_by')
    #     # send_to_id = recevied_message.get('send_to')
    #     response = {
    #         'message': msg+'1'
    #     }
    #     # await self.channel_layer.group_send(
    #     #     self.chat,
    #     #     {
    #     #         'type': 'chat_message',
    #     #         'text': json.dumps(response)
    #     #     }
    #     # )
    #     await self.send(
    #         response
    #     )
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type':'chat_message',
        #         'message':message
        #     }
        # )
        response = {
                    'message': message+'1'
                }
        await self.send(json.dumps(response))
    async def websocket_disconnect(self, event):
        print('disconnect', event)
    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))