import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import CustomUser

# Store connected players by room
players = {}

class MetaverseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'metaverse'
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']

        if message_type == 'player_move':
            # Broadcast player movement to all clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'player_move',
                    'user_id': self.scope['user'].id,
                    'x': text_data_json['x'],
                    'y': text_data_json['y']
                }
            )
        elif message_type == 'chat':
            # Broadcast chat message to all clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat',
                    'user_id': self.scope['user'].id,
                    'message': text_data_json['message']
                }
            )

    async def player_move(self, event):
        # Send player movement to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'player_move',
            'user_id': event['user_id'],
            'x': event['x'],
            'y': event['y']
        }))

    async def chat(self, event):
        # Send chat message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'user_id': event['user_id'],
            'message': event['message']
        }))

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope.get('url_route', {}).get('kwargs', {}).get('room_name', 'default')
        self.room_group_name = f'metaverse_{self.room_name}'
        self.player_id = None

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(f"WebSocket connected to room: {self.room_name}")
        await self.accept()

        # Initialize room if it doesn't exist
        if self.room_name not in players:
            players[self.room_name] = {}

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Remove player from the room
        if self.player_id and self.room_name in players:
            if self.player_id in players[self.room_name]:
                del players[self.room_name][self.player_id]

                # Notify other players that this player has left
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'player_leave',
                        'player_id': self.player_id
                    }
                )

        print(f"WebSocket disconnected from room {self.room_name} with code: {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        print(f"Received in room {self.room_name}: {text_data}")
        if text_data == 'ping':
            await self.send(text_data='pong!')
            return

        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            # Store player_id from the first message
            if 'player_id' in data and not self.player_id:
                self.player_id = data['player_id']

            if message_type == 'player_move':
                # Handle player movement
                await self.handle_player_move(data)
            elif message_type == 'chat_message':
                # Handle chat messages
                await self.handle_chat_message(data)
            elif message_type == 'get_players':
                # Send list of players in the room
                await self.send_player_list()
        except json.JSONDecodeError:
            print(f"Invalid JSON received: {text_data}")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    async def handle_player_move(self, data):
        player_id = data.get('player_id')
        x = data.get('x')
        y = data.get('y')
        direction = data.get('direction', 'down')
        frame = data.get('frame', 0)

        # Store player position
        if self.room_name not in players:
            players[self.room_name] = {}

        players[self.room_name][player_id] = {
            'x': x,
            'y': y,
            'direction': direction,
            'frame': frame
        }

        # Broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_position',
                'player_id': player_id,
                'x': x,
                'y': y,
                'direction': direction,
                'frame': frame
            }
        )

    async def handle_chat_message(self, data):
        player_id = data.get('player_id')
        message = data.get('message', '')

        # Broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'player_id': player_id,
                'message': message
            }
        )

    async def send_player_list(self):
        if self.room_name in players:
            await self.send(text_data=json.dumps({
                'type': 'player_list',
                'players': list(players[self.room_name].keys())
            }))

    # Handlers for messages from the group

    async def player_position(self, event):
        # Send player position to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'player_position',
            'player_id': event['player_id'],
            'x': event['x'],
            'y': event['y'],
            'direction': event.get('direction', 'down'),
            'frame': event.get('frame', 0)
        }))

    async def chat_message(self, event):
        # Send chat message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'player_id': event['player_id'],
            'message': event['message']
        }))

    async def player_leave(self, event):
        # Send player leave notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'player_leave',
            'player_id': event['player_id']
        }))