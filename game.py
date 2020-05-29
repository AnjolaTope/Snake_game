import math
import random
import pygame 
import tkinter as tk
from tkinter import messagebox

class Cube(object):
    rows = 20
    w = 500

    def __init__(self,start,dirnx = 1, dirny = 0, color=(255,0,0)):
        self.position = start 
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        


    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.position = (self.position[0]+self.dirnx, self.position[1] + self.dirny)
        

    def draw (self,surface, eyes =False):
        dis = self.w // self.rows
        i = self.position[0]
        j = self.position[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

        

class Snake(object):
    body = [ ]
    turns = { }

    def __init__(self, color, position):
        self.color = color
        self.head = Cube(position)   #this is the head of the snake , and we need to be able to track it at all times
        self.body.append(self.head) # we need to append the head to the body 
        self.dirnx =   0  #direction  the snake moves
        self.dirny =   1  #the direction the snake moves
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()


            #WE define what happens when we click a key (we change the direction according to the key we press )
            for key in keys:
                if keys [pygame.K_LEFT]:
                    #since we are moving left the x coordinate has to be negative
                    self.dirnx =-1
                    #we only change one direction, because we dont wnat to be moving in multiple directiions
                    self.dirny = 0
                    # we need to remeber were we turned, so that the tail of our snake tails
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]
                elif keys [pygame.K_RIGHT]:
                    #since we are moving right the x coordinate has to be positive
                    self.dirnx = 1
                    #we only change one direction, because we dont wnat to be moving in multiple directiions
                    self.dirny = 0
                    # we need to remeber were we turned, so that the tail of our snake tails
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]
                elif keys [pygame.K_UP]:
                    #we only change one direction, because we dont wnat to be moving in multiple directiions              
                    self.dirnx = 0
                    #since we are moving up the y coordinate has to be positive / negative
                    self.dirny = -1 # 1 
                    # we need to remeber were we turned, so that the tail of our snake tails
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]
                elif keys [pygame.K_DOWN]:
                    #we only change one direction, because we dont wnat to be moving in multiple directiions              
                    self.dirnx = 0
                    #since we are moving down the y coordinate has to be negative /positive 
                    self.dirny = 1 #-1 
                    # we need to remeber were we turned, so that the tail of our snake tails
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

         # moving the cube        
        for i , c in enumerate (self.body) :
            #i is the index, while c is cube index
            #[:] this makes a copy, so we dont change the actual values
            #we ant to get the index and the position of the cube object in the snake position
            # we wan to see if the position is in the turn list 

            p = c.position[:]

            if p in self.turns:
                # we put the directions the snake has to turn in a turn varaible 
                turn =self.turns[p]
                # we use this to move the snake
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    # we reomve that turn from the list
                    self.turns.pop(p)
            else:
                #we are checking if we have reached the end of the screen, so that we can change the position of the snake 
                if c.dirnx == -1 and c.position[0] <= 0: c.position = (c.rows-1, c.position[1])
                elif c.dirnx == 1 and c.position[0] >= c.rows-1: c.position = (0,c.position[1])
                elif c.dirny == 1 and c.position[1] >= c.rows-1: c.position = (c.position[0], 0)
                elif c.dirny == -1 and c.position[1] <= 0: c.position = (c.position[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)





    def reset  (self,position):
        self.head = Cube(position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
      

    def addCube(self):
        tail = self.body[-1]
        dx,dy = tail.dirnx , tail.dirny

        #checks the direction we are moving in so we know when to add the cube and give it the currect direction
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.position[0]-1,tail.position[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.position[0]+1,tail.position[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.position[0],tail.position[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.position[0],tail.position[1]+1)))
 
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
       

    def draw(self,surface)    :
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface,True)
            else:
                c.draw(surface)
           

def drawGrid ( w,rows, surface):
    sizeBtwn =  w // rows 
    x = 0
    y =0 

    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        
        #draws a vertical line
        pygame.draw.line(surface, (255,255,255), (x,0), (x,w))
        #draws a horizontal line
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y))

def redrawWindow(surface):
    global rows, width , s,snack
    surface.fill((0,0,0))  # fills the scrren with color black
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)  # this will draw the gir 
    pygame.display.update() #updates the window

def randomsnack(rows,item):
    positions = item.body

    while True:
         x = random.randrange(rows)
         y= random.randrange(rows)
         # this prvents us from generating a snack on the current possition of the snakw
         if len(list(filter(lambda z:z.position == (x,y) , positions))) > 0:
             continue
         else:
              break

    return(x,y)

 
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
 
def main():
    global rows, width, s ,snack
    width =  500 #the width of the window
    rows = 20    #number of rows for the game
    win = pygame.display.set_mode((width,width)) #this is the surface of the game
    s = Snake((255,0,0), (10,10))
    snack = Cube(randomsnack(rows,s), color = (0,250,0))
    flag = True

    clock = pygame.time.Clock() #allows us to monitor time

    while flag:
        pygame.event.get()
        #delays the program so that the program does not run to fast 
        pygame.time.delay(50)
        #ensures our game does not run more than 10 frames per second 
        clock.tick(10)
        s.move()
        if s.body[0].position ==snack.position:
            s.addCube()
            snack = Cube(randomsnack(rows,s), color = (0,250,0))

        for x in range(len(s.body)):
            if s.body[x].position in list(map(lambda z:z.position,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box(' You lost' , 'Play again')
                s.reset((10,10))
                break


        redrawWindow(win)




main()