from network import Handler, poll
import sys
from threading import Thread
from time import sleep


myname = raw_input('What is your name? ')

class Client(Handler):
    
    def on_close(self):
        print '**** Disconnected from server ****'
        
    def on_msg(self, msg):
        print msg
        
host, port = 'localhost', 8888
client = Client(host, port)
client.do_send({'msg_type' : 'join',
                'user_name' : myname})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
                            
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

while 1:
    mytxt = sys.stdin.readline().rstrip()
    client.do_send({'msg_type' : 'chat',
                    'user_name' : myname, 
                    'txt' : mytxt})
