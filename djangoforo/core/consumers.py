
import json

# Vamos a importar AsyncWebsocketConsumer para crear el consumer
from channels.generic.websocket import AsyncWebsocketConsumer 
# Esto va a servir para guardar los mensajes en la base de datos
from asgiref.sync import sync_to_async 

from users.models import User

from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    # Cada vez que nos conectemos vamos a usar esta funcion
    async def connect(self):
        # Esta va a ser la url a la que nos vamos a intenetar conectar
        self.room_name = self.scope['url_route']['kwargs']['pk']
        # Vmaos a poner chat y el room_name
        self.room_group_name = 'chat_%s' % self.room_name

        # Lugo podemos usar esto para conectarnos 
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # y con esto nos conectamos al servidor
        await self.accept()


    # aqui vamos a crear una funcion apra desconectarnos
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        ) # Crear routing.py

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(pk=room)

        Message.objects.create(user=user, room=room, content=message)