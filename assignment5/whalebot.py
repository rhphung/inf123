from random import randint
from time import sleep
from common import Model

################### CONTROLLER #############################

class Controller():
    def __init__(self, m):
        self.m = m
        self.rand = randint(0,3)
        self.p = self.m.pellets[self.rand]
        
    def handler(self):
        print 'Here you go'
        
    def poll(self):
        x = self.p[0]
        y = self.p[1]

        if y < self.m.mybox[1]:
            self.m.do_cmd('up')
        elif y > self.m.mybox[1]:
            self.m.do_cmd('down')
        elif x > self.m.mybox[0]:
            self.m.do_cmd('right')
        elif x < self.m.mybox[0]:
            self.m.do_cmd('left')
            
        if self.m.pellets[self.rand][0] != x or self.m.pellets[self.rand][1] != y:
            self.rand = randint(0,3)
            self.p = self.m.pellets[self.rand]
        
################### VIEW #############################

import pygame

class View():
    def __init__(self, m):
        self.m = m
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        self.tick = 0
        
    def display(self):
        
        screen = self.screen
        borders = [pygame.Rect(b[0], b[1], b[2], b[3]) for b in self.m.borders]
        pellets = [pygame.Rect(p[0], p[1], p[2], p[3]) for p in self.m.pellets]
        b = self.m.mybox
        myrect = pygame.Rect(b[0], b[1], b[2], b[3])
        
        screen.fill((0, 0, 64))  # dark blue
        pygame.draw.rect(screen, (0, 191, 255), myrect)  # Deep Sky Blue
        [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
        [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
        
        self.tick+=1
        if self.tick == 50:
            print str(myrect[0]) + ', ' + str(myrect[1])
            self.tick = 0
        pygame.display.update()
    
################### LOOP #############################

model = Model()
c = Controller(model)
v = View(model)

while not model.game_over:
    sleep(0.02)
    c.poll()
    model.update()
    v.display()