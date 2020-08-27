import json
from channels.generic.websocket import WebsocketConsumer

class ProgressBarConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("here")
        print(self)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))