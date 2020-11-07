import json
import time
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        counter = 0

        while counter < 20:
            self.send(text_data=f'count: {counter}')
            time.sleep(1)
            counter += 1

        self.close()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.send(text_data='works')