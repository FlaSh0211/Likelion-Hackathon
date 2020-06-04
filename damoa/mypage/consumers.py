# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import datetime
from auction.models import Write,Bid

time = []
alerts = []
alertsid=[]
blog = []
counts  = 0
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        # username = text_data_json['username']
        count = text_data_json['count']
        userid = text_data_json['userid']
      
        counts = int(count)
        userid = int(userid)
        alerts.clear()
        alertsid.clear()
        user_id = userid
        bids = Bid.objects.filter(userId_id = user_id)
        w_id =[]
        for bid in bids:
            w_id.append(bid.writerId)
        
        for i in  w_id:
            if counts == 1 and datetime.datetime.now() > i.e_date and i.confirm == False and i.read == False:
                alerts.append(i.title)
                alertsid.append(i.id)   
                i.confirm = True
                i.save()
                
            elif counts == 1 and datetime.datetime.now() > i.e_date and i.confirm == True and i.read == False:
                alerts.append(i.title)
                alertsid.append(i.id)
                i.confirm = True
                i.save()
            elif counts != 1 and  i.confirm == False and datetime.datetime.now() > i.e_date:
                alerts.append(i.title)
                alertsid.append(i.id)
                i.confirm = True
                i.save()
        count = str(counts + 1)      
         # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
                {
                'type': 'chat_message',
                # 'message': message,
                # 'username': username,
                'alerts':alerts,
                'count':count,
                'alertsid':alertsid,
                
                
                                
            }
        )
       
    
    # Receive message from room group
    def chat_message(self, event):
        # message = event['message']
        # username = event['username']
        count = event['count']       
    
       
 
        

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            # 'message': message,
            # 'username': username,
            'alerts':alerts, 
            'count':count,
            'alertsid':alertsid,
           
           

        }))