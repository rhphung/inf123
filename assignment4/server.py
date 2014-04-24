from network import Listener, Handler, poll

 
handlers = {}  # map client handler to user name

def broadcast(user_name, msg):
    for key, value in handlers.items():
        if key != user_name:
            value.do_send(msg)

class MyHandler(Handler):
     
    def on_open(self):
        print 'server on open'
         
    def on_close(self):
        print 'server on close'
     
    def on_msg(self, msg):
        msg_type = msg['msg_type']
        
        if msg_type == 'join':
            handlers.update({msg['user_name'] : self})
            broadcast('',msg['user_name'] + ' joined. Users: ' + ('%s' % ', '.join(handlers.keys())))
        elif msg_type == 'chat':
            user_name = msg['user_name']
            txt = msg['txt']
            if txt == 'quit':
                value = handlers.pop(user_name)
                broadcast(user_name, user_name + " has left the room. Users: " + ('%s' % ', '.join(handlers.keys())))
                value.do_close()
            else:
                broadcast(msg['user_name'], user_name + ': ' + txt)
 
 
port = 8888
server = Listener(port, MyHandler)

print("Chat server started on port: " + str(port))
while 1:
    poll(timeout=0.05) # in seconds


