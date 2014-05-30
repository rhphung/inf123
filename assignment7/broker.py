from network import Listener, Handler, poll


handlers = {}  # map client handler to user name
names = {} # map name to handler
subs = {} # map tag to handlers

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)


class MyHandler(Handler):
    
    def on_open(self):
        handlers[self] = None
        
    def on_close(self):
        name = handlers[self]
        del handlers[self]
        broadcast({'leave': name, 'users': handlers.values()})
        
    def on_msg(self, msg):
        if 'join' in msg:
            name = msg['join']
            handlers[self] = name
            names[name] = self
            broadcast({'join': name, 'users': handlers.values()})
            #print handlers
            print names
            
        elif 'speak' in msg:
            name, txt = msg['speak'], msg['txt']
            
            #Subscribe
            if "+" in txt:
                word_list = txt.split(" ")
                for word in word_list:
                    if '+' in word:
                        sub = word.replace("+", "")
                        if subs.has_key(sub):
                            subs[sub].append(self)
                        else:
                            subs[sub] = [self]
                        word_list.remove(word)
                txt = " ".join(word_list)
                
            #Unsubscribe
            if '-' in txt:
                word_list = txt.split(" ")   
                for word in word_list:
                    if '-' in word:
                        unsub = word.replace("-", "")
                        if subs.has_key(unsub):
                            subs[unsub].remove(self)
                        word_list.remove(word)
                txt = " ".join(word_list)
                
            #Publish
            if '#' in txt or '@' in txt:
                word_list = txt.split(" ")
                send_list = []
                for word in word_list:
                    if '#' in word:
                        pub = word.replace("#", "")
                        temp = subs.get(pub)
                        if temp != None:
                            for h in temp:
                                if h not in send_list:
                                    send_list.append(h)
                    #Private Publish
                    if '@' in word:
                        privpub = word.replace("@", "")
                        if names.has_key(privpub):
                            privhandler = names[privpub]
                            if privhandler not in send_list:
                                send_list.append(privhandler)
                if send_list != None:
                    for h in send_list:
                        h.do_send({'speak': name, 'txt' : txt})
        
            #No topic in msg
            if "#" not in txt and "+" not in txt and "-" not in txt and "@" not in txt and txt != "":
                broadcast({'speak': name, 'txt': txt})


Listener(8888, MyHandler)
while 1:
    poll(0.05)