from network import Handler, poll
import sys
from threading import Thread
from time import sleep


myname = raw_input('What is your name? ')

done = False

class Client(Handler):
    
    def on_close(self):
        print '**** Disconnected from server ****'
        #self.close_when_done()
        #global done
        #done = True
        #sys.exit()
        
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


while not done:
    try:
        mytxt = sys.stdin.readline().rstrip()
        client.do_send({'msg_type' : 'chat',
                    'user_name' : myname, 
                    'txt' : mytxt})
        if mytxt == 'quit':
            client.on_close()
            done = True
    except (KeyboardInterrupt, SystemExit):
        client.on_close()
        sys.exit()