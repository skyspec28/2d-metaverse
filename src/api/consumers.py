import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connected!")
        await self.accept()

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code: {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        print(f"Received: {text_data}")
        if text_data == 'ping':
            await self.send(text_data='pong!')
            return

        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'player_move':
                # Handle player movement
                await self.handle_player_move(data)
        except json.JSONDecodeError:
            print(f"Invalid JSON received: {text_data}")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    async def handle_player_move(self, data):
        # In a real implementation, we would update the player's position in the database
        # and broadcast the update to all other players in the same space
        player_id = data.get('player_id')
        x = data.get('x')
        y = data.get('y')

        # For now, just echo back the data
        await self.send(text_data=json.dumps({
            'type': 'player_position',
            'player_id': player_id,
            'x': x,
            'y': y
        }))