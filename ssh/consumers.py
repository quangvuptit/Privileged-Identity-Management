# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.contrib.auth.models import User
import paramiko
from .models import SSHPermission ,SSH, BlackList, AccessSSH, TimeBlackList, LogCommand
from django.shortcuts import get_object_or_404
import datetime
from datetime import datetime
from django.core import signing
client = paramiko.SSHClient()


class SSHConsumer(WebsocketConsumer):
    status = False
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'chat_%s' % self.room_name
        self.idSSH = self.scope['path'].split('/')[3]
        self.user = self.scope['user']
        self.s = SSH.objects.get(pk=self.idSSH)
        if not self.user.is_staff:
            obj, created = AccessSSH.objects.get_or_create(ssh=self.s, user = self.scope['user'])
        else:
            created = True    
        if created:
            if created:
                LogCommand.objects.create(user=self.scope['user'], connection= self.s)
            async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        AccessSSH.objects.filter(ssh=self.s).delete()
        self.close()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message.split(":")[0]=='connect' :
            statusConnect = SSHManage.connectSSH(self, message.split(":")[1])
            if statusConnect==1 :
                self.send(text_data=json.dumps({
                    'message':'Connect successfully' 
                    }))
            else:
                self.send(text_data=json.dumps({
                    'message':'Connect fail !'
                    })) 
        elif message=='disconnect' :
            self.close()
            SSHManage.disconnect(self)        
        else:        
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
                {
                'type': 'chat_message',
                'message': message
                }
            )     
        
    def chat_message(self, event):
        message = event['message']
        logcmd = LogCommand.objects.filter(user=self.scope['user'],connection=self.s).latest('logTime')
        logcmd.command +=(message+'||||')
        logcmd.save()
       
        self.send(text_data=json.dumps({
                'message': message
                }))
        sp = message.split('|')
        check = -1
        for i in sp:
            # if BlackList.objects.filter(keyword=i.strip()):
            #     check = i
            bl = BlackList.objects.filter(keyword=i.strip())
            if bl:
                cmd = TimeBlackList.objects.filter(cmd__keyword=i.strip(), ssh=self.s)
                if cmd:
                    cmd = TimeBlackList.objects.get(cmd__keyword=i.strip(), ssh=self.s)
                    now = datetime.now().strftime('%H:%M:%S')
                    date_now = datetime.strptime(now,'%H:%M:%S').time()
                    if cmd.startTime <= date_now and cmd.endTime >= date_now:
                        check = -1
                    else:
                        check = 1
                else:
                    check = i                                       
        if check != -1:
            errorMessage = 'Command "' +i + '" is not allowed!'
            self.send(text_data=json.dumps({
                'message':errorMessage
                }))
        else:
            SSHManage.command(self, message) 	
class SSHManage:
    def connectSSH(self , id):
    	
    	obj = get_object_or_404(SSH, id=id)
    	client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    	try:
    		client.connect(obj.ip, port=obj.port, username=obj.username,password=signing.loads(obj.password))
    	except:
    		return 0	
    	return 1;    
    def disconnect(self):
    	client.close()

    def command(self, message):
        if message.split(' ')[0]=='cat':
            sftp_client = client.open_sftp()
            remote_file = sftp_client.open(message.split(' ')[1])
            try:
                for line in remote_file:
                    self.send(text_data=json.dumps({
                        'message':line.rstrip()
                        }))
            finally:
                remote_file.close()        
        else:    
            stdin, stdout, stderr = client.exec_command(message)
            for line in stdout:
                self.send(text_data=json.dumps({
                    'message':line.rstrip()
    			}))   		