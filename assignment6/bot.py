from time import sleep
from network import Handler, poll
from pygame import Rect

global connected
connected = False

################### MODEL #############################

def make_rect(quad):  # make a pygame.Rect from a list of 4 integers
    x, y, w, h = quad
    return Rect(x, y, w, h)

class Model():
    
    borders = []
    pellets = []
    players = {}
    myname = None
    game_over = False
    got_bigger = False
    mybot = [0, 0, 10, 10]
    prev_bot = mybot
    mydir = 'down'
    
    def do_cmd(self, cmd):
        if cmd == 'quit':
            self.connected = False
            self.game_over = True
        else:
            self.mydir = cmd
    
    def update(self, data):
        self.borders = [make_rect(b) for b in data['borders']]
        self.pellets = [make_rect(p) for p in data['pellets']]
        self.players = {name: make_rect(p) for name, p in data['players'].items()}
        self.myname = data['myname']
        self.prev_bot = self.mybot
        self.mybot = self.players[self.myname]
        

################### BOT CONTROLLER ##########################

class SmartBotController():
    def __init__(self, m):
        self.m = m
        
    def poll(self):
        p = self.m.pellets[0]  # always target the first pellet
        b = self.m.players[self.m.myname]
        
        if p[0] > b[0]:
            cmd = 'right'
        elif p[0] + p[2] < b[0]: # p[2] to avoid stuttering left-right movement
            cmd = 'left'
        elif p[1] > b[1]:
            cmd = 'down'
        else:
            cmd = 'up'

        self.m.do_cmd(cmd)
        

################### CLIENT CONTROLLER ######################


class ClientController(Handler):
    
    def addModel(self, m):
        self.m = m
        #self.v = v
        
    def on_open(self):
        #self.v.on_connect()
        self.m.connected = True
        
    def on_close(self):
        self.m.connected = False
        self.m.game_over = True
        #self.v.on_disconnect()
            
    def on_msg(self, data):
        #print data
        self.m.update(data)
        
    def send_msg(self, msg):
        self.do_send(msg)
        #print 'here'

################### CONSOLE VIEW #############################

class ConsoleView():
    def __init__(self, m):
        self.m = m
        self.printed = False
    
    def on_connect(self):
        print '***** client connected *****'
        
    def on_disconnect(self):
        print '***** client disconnected *****'
            
    def display(self):
        if self.m.connected and self.printed == False:
            print '***** client connected *****'
            self.printed = True
            
        if self.m.game_over and self.m.connected == False:
            print '***** client disconnected *****'
            
        if self.m.prev_bot[2] != self.m.mybot[2] and self.m.prev_bot[3] != self.m.mybot[3] and self.m.got_bigger == False:
            #print str(self.m.prev_bot[2]) + " " + str(self.m.prev_bot[3])
            #print str(self.m.mybot[2]) + " " + str(self.m.mybot[3])
            self.m.got_bigger = True
            print 'Pellet was eaten!'
        else:
            self.m.got_bigger = False

# Check that bot gets bigger in view


################### PYGAME VIEW #############################
# this view is only here in case you want to see how the bot behaves

import pygame

class PygameView():
    
    def __init__(self, m):
        self.m = m
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
    
    def display(self):
        pygame.event.pump()
        screen = self.screen
        borders = [pygame.Rect(b[0], b[1], b[2], b[3]) for b in self.m.borders]
        pellets = [pygame.Rect(p[0], p[1], p[2], p[3]) for p in self.m.pellets]
        screen.fill((0, 0, 64))  # dark blue
        for name, p in self.m.players.items():
            if name != self.m.myname:
                pygame.draw.rect(screen, (255, 0, 0), p)  # red
            if self.m.myname:
                pygame.draw.rect(screen, (0, 191, 255), self.m.players[self.m.myname])  # deep sky blue
        [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
        [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
        pygame.display.update()
        
################### LOOP #############################

model = Model()
console = ConsoleView(model)
client = ClientController('localhost', 8888)  # connect asynchronously
client.addModel(model)
bot = SmartBotController(model)
v2 = PygameView(model)
    
while not model.game_over:
    sleep(0.02)
    
    poll()
    bot.poll()
    #print 'after poll'
    client.send_msg({'input': model.mydir})
    #print 'after send msg'
    console.display()
    #print 'after display'
    v2.display()

