from shutil import register_unpack_format
from turtle import reset
import pygame
import random
import copy
import threading as mt
import time

def drawGrid(): 
    blockSize = 30 #Set the size of the grid block
    for x in range(300, 600, blockSize):
        for y in range(300, 900, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, GREY, rect, 1)

class particlePolygon:
    def __init__(self, x, y, color, shrink):
        self.particles = []
        self.x = x
        self.y = y
        self.color = color
        self.shrink = shrink

    def addParticle(self):
        radius = 5
        directionX = random.randint(-2, 2)
        directionY = random.randint(-2, 2)
        particlePolygon = [[self.x, self.y-radius], [self.x+radius, self.y], [self.x, self.y+radius], [self.x-radius, self.y], radius, [directionX, directionY]]
        self.particles.append(particlePolygon)

    def emit(self):
        if self.particles:
            self.deleteParticles()
            for particle in self.particles:
                particle[0][1] += self.shrink
                particle[1][0] -= self.shrink
                particle[2][1] -= self.shrink #shrink the polygon
                particle[3][0] += self.shrink
                particle[4] -= self.shrink

                particle[0][0] += particle[5][0]
                particle[1][0] += particle[5][0] #random move in x axis
                particle[2][0] += particle[5][0]
                particle[3][0] += particle[5][0]

                particle[0][1] += particle[5][1]
                particle[1][1] += particle[5][1] #random move in y axis
                particle[2][1] += particle[5][1]
                particle[3][1] += particle[5][1]
                
                pygame.draw.polygon(screen, self.color, [particle[0], particle[1], particle[2], particle[3]])
                pygame.display.update()

    def deleteParticles(self):
        particleCopy = [particle for particle in self.particles if particle[4] > 0.2]
        self.particles = particleCopy

def generateParticles(lines, xCoord, color, shrink, amount):
    yay = []
    if xCoord: #specific x coordinate provided
        for n in range (0, amount):
            for y in lines:
                yay.append(particlePolygon(xCoord+15, y+15, color, shrink)) #5 particles for each tile
    else: #cover the entire row
        for x in range(300, 600, 30):
            for n in range (0, amount):
                for y in lines:
                    yay.append(particlePolygon(x+15, y+15, color, shrink)) #5 particles for each tile
    print(len(yay))
    for i in yay:
        i.addParticle() #add the particle for each particle
    for n in range(0, 100):
        for i in range(0, 2):
            screen.fill(BLACK) #fill in the black background
            #dropPredict() #update the drop predict
            drawShape() #draw the urrent piece after the shifts
            drawPastShape() #draw all the previously dropped pieces
            #pygame.draw.rect(screen, [255, 0, 255], bottom)
            drawGrid()
            pygame.draw.line(screen, WHITE, (300, 300), (300, 900), 5)
            pygame.draw.line(screen, WHITE, (298, 900), (602, 900), 5)
            pygame.draw.line(screen, WHITE, (600, 300), (600, 900), 5)
            #pygame.display.update()

            for i in range(0, len(yay)):
                yay[i].emit()
    yay.clear()

def tSpinParticles():
    global newShape
    a = pygame.Rect(newShape.three.x - 30, newShape.three.y - 30, 30, 30)
    b = pygame.Rect(newShape.three.x + 30, newShape.three.y - 30, 30, 30)
    c = pygame.Rect(newShape.three.x - 30, newShape.three.y + 30, 30, 30)
    d = pygame.Rect(newShape.three.x + 30, newShape.three.y + 30, 30, 30)
    if (detectCollision(a) + detectCollision(b) + detectCollision(c) + detectCollision(d)) >= 3: 
        generateParticles([newShape.three.y], newShape.three.x, (255, 0, 255), 0.5, 10)

"""def hardDropParticles():
    t1 = mt.Thread(target=hardDropParticle1, args=())
    t2 = mt.Thread(target=hardDropParticle2, args=())
    t3 = mt.Thread(target=hardDropParticle3, args=())
    t4 = mt.Thread(target=hardDropParticle4, args=())
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()

def hardDropParticle1():
    if touchingBottom(newShape.one) or touchingExisting_bottom(newShape.one):
        generateParticles([newShape.one.y+15], newShape.one.x, WHITE, 0.5, 2)
def hardDropParticle2():
    if touchingBottom(newShape.two) or touchingExisting_bottom(newShape.two):
        generateParticles([newShape.two.y+15], newShape.two.x, WHITE, 0.5, 2)
def hardDropParticle3():
    if touchingBottom(newShape.three) or touchingExisting_bottom(newShape.three):
        generateParticles([newShape.three.y+15], newShape.three.x, WHITE, 0.5, 2)
def hardDropParticle4():
    if touchingBottom(newShape.four) or touchingExisting_bottom(newShape.four):
        generateParticles([newShape.four.y+15], newShape.four.x, WHITE, 0.5, 2)"""

class O:
    one = pygame.Rect(420, 210, 30, 30)
    two = pygame.Rect(450, 210, 30, 30)
    three = pygame.Rect(450, 240, 30, 30)
    four = pygame.Rect(420, 240, 30, 30)
    rotation = [0, 0]
    color = [255, 255, 0] #yellow
    name = 'O'

class I:
    one = pygame.Rect(390, 240, 30, 30)
    two = pygame.Rect(420, 240, 30, 30)
    three = pygame.Rect(450, 240, 30, 30)
    four = pygame.Rect(480, 240, 30, 30)
    rotation = [0, 0]
    color = [0, 255, 255] #cyan 
    name = 'I'

class T:
    one = pygame.Rect(420, 210, 30, 30)
    two = pygame.Rect(390, 240, 30, 30)
    three = pygame.Rect(420, 240, 30, 30)
    four = pygame.Rect(450, 240, 30, 30)
    rotation = [0, 0]
    color = [128, 0, 128] #purple
    name = 'T'

class S:
    one = pygame.Rect(420, 210, 30, 30)
    two = pygame.Rect(450, 210, 30, 30)
    three = pygame.Rect(390, 240, 30, 30)
    four = pygame.Rect(420, 240, 30, 30)
    rotation = [0, 0]
    color = [0, 255, 0] #green
    name = 'S'

class Z:
    one = pygame.Rect(390, 210, 30, 30)
    two = pygame.Rect(420, 210, 30, 30)
    three = pygame.Rect(420, 240, 30, 30)
    four = pygame.Rect(450, 240, 30, 30)
    rotation = [0, 0]
    color = [255, 0, 0] #red
    name = 'Z'

class J:
    one = pygame.Rect(390, 210, 30, 30)
    two = pygame.Rect(390, 240, 30, 30)
    three = pygame.Rect(420, 240, 30, 30)
    four = pygame.Rect(450, 240, 30, 30)
    rotation = [0, 0]
    color = [0, 0, 255] #blue
    name = 'J'

class L:
    one = pygame.Rect(390, 240, 30, 30)
    two = pygame.Rect(420, 240, 30, 30)
    three = pygame.Rect(450, 240, 30, 30)
    four = pygame.Rect(450, 210, 30, 30)
    rotation = [0, 0]
    color = [255, 127, 0] #orange
    name = 'L'

def drawShape():
    pygame.draw.rect(screen, newShape.color, newShape.one)
    pygame.draw.rect(screen, newShape.color, newShape.two)
    pygame.draw.rect(screen, newShape.color, newShape.three)
    pygame.draw.rect(screen, newShape.color, newShape.four)
    
def checkDropped():
    global dropped, frameCount, droppedTime
    if dropped == True:
        if not touchingBottom(None) and not touchingExisting_bottom(None):
            print("e")
            dropped = False
            droppedTime = 0
    elif touchingBottom(None) or touchingExisting_bottom(None):
        dropped = True
        droppedTime = frameCount
        return

def newPiece():
    global newShape, bag, dropped, queue, holdLock
    if not bag:
        bag = [O, I, T, J, L, S , Z]
    while len(queue) < 5:
        queue.append(random.choice(bag))
        bag.remove(queue[-1])
    print(queue)
    print(bag)
    newShape = queue[0]; queue.pop(0)
    dropped = False; holdLock = False

def hold():
    global newShape, holdPiece, holdLock
    if holdLock:
        return
    if not holdPiece:
        resetPiece()
        holdPiece = newShape
        newPiece()
        holdLock = True
    else:
        resetPiece()
        holdPiece, newShape = newShape, holdPiece
        holdLock = True
 
def moveDown():
    global newShape
    newShape.one.y += 30
    newShape.two.y += 30
    newShape.three.y += 30
    newShape.four.y += 30

def moveUp():
    global newShape
    newShape.one.y -= 30
    newShape.two.y -= 30
    newShape.three.y -= 30
    newShape.four.y -= 30

def moveLeft():
    global newShape
    newShape.one.x -= 30
    newShape.two.x -= 30
    newShape.three.x -= 30
    newShape.four.x -= 30

def moveRight():
    global newShape
    newShape.one.x += 30
    newShape.two.x += 30
    newShape.three.x += 30
    newShape.four.x += 30

def rotateCCW():
    global newShape
    global lastMove, yCoordinate
    originalOne = copy.copy(newShape.one)
    originalTwo = copy.copy(newShape.two)
    originalThree = copy.copy(newShape.three)
    originalFour = copy.copy(newShape.four)
    originalRotation = copy.copy(newShape.rotation)
    if newShape.name == 'O':
        lastMove = "rotation"
        return #I'm too lazy to code the spin, deal with it
    elif newShape.name == 'I':
        if newShape.rotation[1] == 0: #rotation 0 to 3
            newShape.one.x += 30
            newShape.one.y += 60
            newShape.two.y += 30
            newShape.three.x -= 30
            newShape.four.x -= 60
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 2
            newShape.one.x += 60
            newShape.one.y -= 30
            newShape.two.x += 30
            newShape.three.y += 30
            newShape.four.x -= 30
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 1
            newShape.one.x -= 30
            newShape.one.y -= 60
            newShape.two.y -= 30
            newShape.three.x += 30
            newShape.four.x += 60
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 0
            newShape.one.x -= 60
            newShape.one.y += 30
            newShape.two.x -= 30
            newShape.three.y -= 30
            newShape.four.x += 30
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return

    elif newShape.name == 'T':
        if newShape.rotation[1] == 0: #rotation 0 to 3
            newShape.one.x -= 30
            newShape.one.y += 30
            newShape.two.x += 30
            newShape.two.y += 30
            newShape.four.x -= 30
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; yCoordinate = newShape.three.y; tSpinParticles(); return
        elif newShape.rotation[1] == 3: #rotation 3 to 2
            newShape.one.x += 30
            newShape.one.y += 30
            newShape.two.x += 30
            newShape.two.y -= 30
            newShape.four.x -= 30
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; yCoordinate = newShape.three.y; tSpinParticles(); return
        elif newShape.rotation[1] == 2: #rotation 2 to 1
            newShape.one.x += 30
            newShape.one.y -= 30
            newShape.two.x -= 30
            newShape.two.y -= 30
            newShape.four.x += 30
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; yCoordinate = newShape.three.y; tSpinParticles(); return
        elif newShape.rotation[1] == 1: #rotation 1 to 0
            newShape.one.x -= 30
            newShape.one.y -= 30
            newShape.two.x -= 30
            newShape.two.y += 30
            newShape.four.x += 30
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; yCoordinate = newShape.three.y; tSpinParticles(); return
    elif newShape.name == 'J': 
        if newShape.rotation[1] == 0: #rotation 0 to 3
            newShape.one.y += 60
            newShape.two.x += 30
            newShape.two.y += 30
            newShape.four.x -= 30
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 2
            newShape.one.x += 60
            newShape.two.x += 30
            newShape.two.y -= 30
            newShape.four.x -= 30
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 1
            newShape.one.y -= 60
            newShape.two.x -= 30
            newShape.two.y -= 30
            newShape.four.x += 30
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 0
            newShape.one.x -= 60
            newShape.two.x -= 30
            newShape.two.y += 30
            newShape.four.x += 30
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return

    elif newShape.name == 'L':
        if newShape.rotation[1] == 0: #rotation 0 to 3
            newShape.one.x += 30
            newShape.one.y += 30
            newShape.three.x -= 30
            newShape.three.y -= 30
            newShape.four.x -= 60
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 2
            newShape.one.x += 30
            newShape.one.y -= 30
            newShape.three.x -= 30
            newShape.three.y += 30
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 1:
            newShape.one.x -= 30
            newShape.one.y -= 30
            newShape.three.x += 30
            newShape.three.y += 30
            newShape.four.x += 60
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 0
            newShape.one.x -= 30 
            newShape.one.y += 30
            newShape.three.x += 30
            newShape.three.y -= 30
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return

    elif newShape.name == 'S':
        if newShape.rotation[1] == 0: #rotation 0 to 3
            newShape.one.x -= 30
            newShape.one.y += 30
            newShape.two.x -= 60
            newShape.three.x += 30
            newShape.three.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 2
            newShape.one.x += 30
            newShape.one.y += 30
            newShape.two.y += 60
            newShape.three.x += 30
            newShape.three.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 1
            newShape.one.x += 30
            newShape.one.y -= 30
            newShape.two.x += 60
            newShape.three.x -= 30
            newShape.three.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 0
            newShape.one.x -= 30
            newShape.one.y -= 30
            newShape.two.y -= 60
            newShape.three.x -= 30
            newShape.three.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return

    elif newShape.name == 'Z':
        if newShape.rotation[1] == 0: #rotation 0 to 3
            newShape.one.y += 60
            newShape.two.x -= 30
            newShape.two.y += 30
            newShape.four.x -= 30
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 2
            newShape.one.x += 60
            newShape.two.x += 30
            newShape.two.y += 30
            newShape.four.x -= 30
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 1
            newShape.one.y -= 60
            newShape.two.x += 30
            newShape.two.y -= 30
            newShape.four.x += 30
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 0
            newShape.one.x -= 60
            newShape.two.x -= 30
            newShape.two.y -= 30
            newShape.four.x += 30
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+3)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return

def rotateCW():
    global newShape
    global lastMove, yCoordinate
    originalOne = copy.copy(newShape.one)
    originalTwo = copy.copy(newShape.two)
    originalThree = copy.copy(newShape.three)
    originalFour = copy.copy(newShape.four)
    originalRotation = copy.copy(newShape.rotation)
    if newShape.name == 'O':
        lastMove = "rotation"
        return #I'm too lazy to code the spin, deal with it
    elif newShape.name == 'I':
        if newShape.rotation[1] == 0: #rotation 0 to 1
            newShape.one.x += 60
            newShape.one.y -= 30
            newShape.two.x += 30
            newShape.three.y += 30
            newShape.four.x -= 30
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 2
            newShape.one.x += 30
            newShape.one.y += 60
            newShape.two.y += 30
            newShape.three.x -= 30
            newShape.four.x -= 60
            newShape.four.y -=30
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 3
            newShape.one.x -= 60
            newShape.one.y += 30
            newShape.two.x -= 30
            newShape.three.y -= 30
            newShape.four.x += 30
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shifts the previous rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 0
            newShape.one.x -= 30
            newShape.one.y -= 60
            newShape.two.y -= 30
            newShape.three.x += 30
            newShape.four.x += 60
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
    
    elif newShape.name == 'T':
        if newShape.rotation[1] == 0: #rotation 0 to 1
            newShape.one.x += 30
            newShape.one.y += 30
            newShape.two.x += 30
            newShape.two.y -= 30
            newShape.four.x -= 30
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; yCoordinate = newShape.three.y; tSpinParticles(); return
        elif newShape.rotation[1] == 1: #rotation 1 to 2
            newShape.one.x -= 30
            newShape.one.y += 30
            newShape.two.x += 30
            newShape.two.y += 30
            newShape.four.x -= 30
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; yCoordinate = newShape.three.y; tSpinParticles(); return
        elif newShape.rotation[1] == 2: #rotation 2 to 3
            newShape.one.x -= 30
            newShape.one.y -= 30
            newShape.two.x -= 30
            newShape.two.y += 30
            newShape.four.x += 30
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; yCoordinate = newShape.three.y; tSpinParticles(); return
        elif newShape.rotation[1] == 3: #rotation 3 to 0
            newShape.one.x += 30
            newShape.one.y -= 30
            newShape.two.x -= 30
            newShape.two.y -= 30
            newShape.four.x += 30
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; yCoordinate = newShape.three.y; tSpinParticles(); return

    elif newShape.name == 'J':
        if newShape.rotation[1] == 0: #rotation 0 to 1
            newShape.one.x += 60
            newShape.two.x += 30
            newShape.two.y -= 30
            newShape.four.x -= 30
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 2
            newShape.one.y += 60
            newShape.two.x += 30
            newShape.two.y += 30
            newShape.four.x -= 30
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 3
            newShape.one.x -= 60
            newShape.two.x -= 30
            newShape.two.y += 30
            newShape.four.x += 30
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 0
            newShape.one.y -= 60
            newShape.two.x -= 30
            newShape.two.y -= 30
            newShape.four.x += 30
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return

    elif newShape.name == 'L':
        if newShape.rotation[1] == 0: #rotation 0 to 1
            newShape.one.x += 30
            newShape.one.y -= 30
            newShape.three.x -= 30
            newShape.three.y += 30
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 2
            newShape.one.x += 30
            newShape.one.y += 30
            newShape.three.x -= 30
            newShape.three.y -= 30
            newShape.four.x -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 3
            newShape.one.x -= 30
            newShape.one.y += 30
            newShape.three.x += 30
            newShape.three.y -= 30
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 0
            newShape.one.x -= 30
            newShape.one.y -= 30
            newShape.three.x += 30
            newShape.three.y += 30
            newShape.four.x += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return

    elif newShape.name == 'S':
        if newShape.rotation[1] == 0: #rotation = 0 to 1
            newShape.one.x += 30
            newShape.one.y += 30
            newShape.two.y += 60
            newShape.three.x += 30
            newShape.three.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 2
            newShape.one.x -= 30
            newShape.one.y += 30
            newShape.two.x -= 60
            newShape.three.x += 30
            newShape.three.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 3
            newShape.one.x -= 30
            newShape.one.y -= 30
            newShape.two.y -= 60
            newShape.three.x -= 30
            newShape.three.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 0
            newShape.one.x += 30
            newShape.one.y -= 30
            newShape.two.x += 60
            newShape.three.x -= 30
            newShape.three.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
    elif newShape.name == 'Z':
        if newShape.rotation[1] == 0: #rotation 0 to 1
            newShape.one.x += 60
            newShape.two.x += 30
            newShape.two.y += 30
            newShape.four.x -= 30
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 2
            newShape.one.y += 60
            newShape.two.x -= 30
            newShape.two.y += 30
            newShape.four.x -= 30
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 3
            newShape.one.x -= 60
            newShape.two.x -= 30
            newShape.two.y -= 30
            newShape.four.x += 30
            newShape.four.y -= 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 0
            newShape.one.y -= 60
            newShape.two.x += 30
            newShape.two.y -= 30
            newShape.four.x += 30
            newShape.four.y += 30
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+1)%4 #update current rotation index
            if not wallKick(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return

def rotate180():
    global newShape
    global lastMove, yCoordinate
    originalOne = copy.copy(newShape.one)
    originalTwo = copy.copy(newShape.two)
    originalThree = copy.copy(newShape.three)
    originalFour = copy.copy(newShape.four)
    originalRotation = copy.copy(newShape.rotation)
    if newShape.name == 'O':
        lastMove = "rotation"
        return #no O-spin deal with it
    if newShape.name == 'I':
        if newShape.rotation[1] == 0: #rotation 0 to 2 
            newShape.one.x += 90
            newShape.two.x += 30
            newShape.three.x -= 30
            newShape.four.x -= 90
            moveDown()
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 3
            newShape.one.y += 90
            newShape.two.y += 30
            newShape.three.y -= 30
            newShape.four.y -= 90
            moveLeft()
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 0 
            newShape.one.x -= 90
            newShape.two.x -= 30
            newShape.three.x += 30
            newShape.four.x += 90
            moveUp()
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 1
            newShape.one.y -= 90
            newShape.two.y -= 30
            newShape.three.y += 30
            newShape.four.y += 90
            moveRight()
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return

    elif newShape.name == 'T':
        if newShape.rotation[1] == 0: #rotation 0 to 2
            newShape.one.y += 60
            newShape.two.x += 60
            newShape.four.x -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; yCoordinate = newShape.three.y; tSpinParticles(); return
        elif newShape.rotation[1] == 1: #roation 1 to 3
            newShape.one.x -= 60
            newShape.two.y += 60
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; yCoordinate = newShape.three.y; tSpinParticles(); return
        elif newShape.rotation[1] == 2: #rotation 2 to 0
            newShape.one.y -= 60
            newShape.two.x -= 60
            newShape.four.x += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; yCoordinate = newShape.three.y; tSpinParticles(); return
        elif newShape.rotation[1] == 3: #rotation 3 to 1
            newShape.one.x += 60
            newShape.two.y -= 60
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; yCoordinate = newShape.three.y; tSpinParticles(); return

    elif newShape.name == 'J':
        if newShape.rotation[1] == 0: #rotation 0 to 2
            newShape.one.x += 60
            newShape.one.y += 60
            newShape.two.x += 60
            newShape.four.x -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 3
            newShape.one.x -= 60
            newShape.one.y += 60
            newShape.two.y += 60
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 0
            newShape.one.x -= 60
            newShape.one.y -= 60
            newShape.two.x -= 60
            newShape.four.x += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 1
            newShape.one.x += 60
            newShape.one.y -= 60
            newShape.two.y -= 60
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return

    elif newShape.name == 'L': 
        if newShape.rotation[1] == 0: #rotation 0 to 2
            newShape.one.x += 60
            newShape.three.x -= 60
            newShape.four.x -= 60
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 3
            newShape.one.y += 60
            newShape.three.y -= 60
            newShape.four.x -= 60
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 0
            newShape.one.x -= 60
            newShape.three.x += 60
            newShape.four.x += 60
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 1
            newShape.one.y -= 60
            newShape.three.y += 60
            newShape.four.x += 60
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return

    elif newShape.name == 'S':
        if newShape.rotation[1] == 0: #rotation 0 to 2
            newShape.one.y += 60
            newShape.two.x -= 60
            newShape.two.y += 60
            newShape.three.x += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 3
            newShape.one.x -= 60
            newShape.two.x -= 60
            newShape.two.y -= 60
            newShape.three.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 0
            newShape.one.y -= 60
            newShape.two.x += 60
            newShape.two.y -= 60
            newShape.three.x -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 1
            newShape.one.x += 60
            newShape.two.x += 60
            newShape.two.y += 60
            newShape.three.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
    
    elif newShape.name == 'Z':
        if newShape.rotation[1] == 0: #rotation 0 to 2
            newShape.one.x += 60
            newShape.one.y += 60
            newShape.two.y += 60
            newShape.four.x -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 1: #rotation 1 to 3
            newShape.one.x -= 60
            newShape.one.y += 60
            newShape.two.x -= 60
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 2: #rotation 2 to 0
            newShape.one.x -= 60
            newShape.one.y -= 60
            newShape.two.y -= 60
            newShape.four.x += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return
        elif newShape.rotation[1] == 3: #rotation 3 to 1
            newShape.one.x += 60
            newShape.one.y -= 60
            newShape.two.x += 60
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: lastMove = "rotation"; return

def none():
    return            

wallKickLUT = { #wall kick look up table for T, S, Z, J, L
    "[[0, 1], 2]": (moveLeft), "[[0, 1], 3]": (moveLeft, moveUp), "[[0, 1], 4]": (moveDown, moveDown), "[[0, 1], 5]": (moveLeft, moveDown, moveDown), #rotating from 0 to 1 CW
    "[[1, 0], 2]": (moveRight), "[[1, 0], 3]": (moveRight, moveDown), "[[1, 0], 4]": (moveUp, moveUp), "[[1, 0], 5]": (moveRight, moveUp, moveUp), #rotating from 1 to 0 CCW
    "[[1, 2], 2]": (moveRight), "[[1, 2], 3]": (moveRight, moveDown), "[[1, 2], 4]": (moveUp, moveUp), "[[1, 2], 5]": (moveRight, moveUp, moveUp), #rotating from 1 to 2 CW
    "[[2, 1], 2]": (moveLeft), "[[2, 1], 3]": (moveLeft, moveUp), "[[2, 1], 3]": (moveDown, moveDown), "[[2, 1], 5]": (moveLeft, moveDown, moveDown), #rotating from 2 to 1 CCW
    "[[2, 3], 2]": (moveRight), "[[2, 3], 3]": (moveRight, moveUp), "[[2, 3], 4]": (moveDown, moveDown), "[[2, 3], 5]": (moveRight, moveDown, moveDown), #rotating from 2 to 3 CW
    "[[3, 2], 2]": (moveLeft), "[[3, 2], 3]": (moveLeft, moveDown), "[[3, 2], 4]": (moveUp, moveUp), "[[3, 2], 5]": (moveLeft, moveUp, moveUp), #rotating from 3 to 2 CCW
    "[[3, 0], 2]": (moveLeft), "[[3, 0], 3]": (moveLeft, moveDown), "[[3, 0], 4]": (moveUp, moveUp), "[[3, 0], 5]": (moveLeft, moveUp, moveUp), #rotating from 3 to 0 CW
    "[[0, 3], 2]": (moveRight), "[[0, 3], 3]": (moveRight, moveUp), "[[0, 3], 4]": (moveDown, moveDown), "[[0, 3], 5]": (moveRight, moveDown, moveDown), #rotating from 0 to 3 CCW
}

wallKickLUT_I = { #wall kick look up table for I 
    "[[0, 1], 2]": (moveLeft, moveLeft), "[[0, 1], 3]": (moveRight, none), "[[0, 1], 4]": (moveLeft, moveLeft, moveDown), "[[0, 1], 5]": (moveRight, moveUp, moveUp), #rotating from 0 to 1 CW
    "[[1, 0], 2]": (moveRight, moveRight), "[[1, 0], 3]": (moveLeft, none), "[[1, 0], 4]": (moveRight, moveRight, moveUp), "[[1, 0], 5]": (moveLeft, moveDown, moveDown), #rotating from 1 to 0 CCW
    "[[1, 2], 2]": (moveLeft, none), "[[1, 2], 3]": (moveRight, moveRight), "[[1, 2], 4]": (moveLeft, moveUp, moveUp), "[[1, 2], 5]": (moveRight, moveRight, moveDown), #rotating from 1 to 2 CW
    "[[2, 1], 2]": (moveRight, none), "[[2, 1], 3]": (moveLeft, moveLeft), "[[2, 1], 3]": (moveRight, moveDown, moveDown), "[[2, 1], 5]": (moveLeft, moveLeft, moveUp), #rotating from 2 to 1 CCW
    "[[2, 3], 2]": (moveRight, moveRight), "[[2, 3], 3]": (moveLeft, none), "[[2, 3], 4]": (moveRight, moveRight, moveUp), "[[2, 3], 5]": (moveLeft, moveDown, moveDown), #rotating from 2 to 3 CW
    "[[3, 2], 2]": (moveLeft, moveLeft), "[[3, 2], 3]": (moveRight, none), "[[3, 2], 4]": (moveLeft, moveLeft, moveDown), "[[3, 2], 5]": (moveRight, moveUp, moveUp), #rotating from 3 to 2 CCW
    "[[3, 0], 2]": (moveRight, none), "[[3, 0], 3]": (moveLeft, moveLeft), "[[3, 0], 4]": (moveRight, moveDown, moveDown), "[[3, 0], 5]": (moveLeft, moveLeft, moveUp), #rotating from 3 to 0 CW
    "[[0, 3], 2]": (moveLeft, none), "[[0, 3], 3]": (moveRight, moveRight), "[[0, 3], 4]": (moveLeft, moveUp, moveUp), "[[0, 3], 5]": (moveRight, moveRight, moveDown) #rotating from 0 to 3 CCW
}

wallKickLUT_180 = {
    "[[0, 2], 2]": (moveUp), "[[0, 2], 3]": (moveRight, moveUp, none), "[[0, 2], 4]": (moveLeft, moveUp), "[[0, 2], 5]": (moveRight, none), "[[0, 2], 6]": (moveLeft), #rotating from 0 to 2 CW
    "[[2, 0], 2]": (moveDown), "[[2, 0], 3]": (moveLeft, moveDown, none), "[[2, 0], 4]": (moveRight, moveDown), "[[2, 0], 5]": (moveLeft, none), "[[2, 0], 6]": (moveRight), #rotating from 2 to 0 CCW
    "[[1, 3], 2]": (moveRight), "[[1, 3], 3]": (moveRight, moveUp, moveUp), "[[1, 3], 4]": (moveRight, moveUp), "[[1, 3], 5]": (moveUp, moveUp), "[[1, 3], 6]": (moveUp), #rotating from 1 to 3 CW
    "[[3, 1], 2]": (moveLeft), "[[3, 1], 3]": (moveLeft, moveUp, moveUp), "[[3, 1], 4]": (moveLeft, moveUp), "[[3, 1], 5]": (moveUp, moveUp), "[[3, 1], 6]": (moveUp) #rotating from 3 to 1 CCW
}

def wallKick(): #check if the rotation is valid, if not, test the wall kicks 
    global newShape
    originalOne = copy.copy(newShape.one)
    originalTwo = copy.copy(newShape.two)
    originalThree = copy.copy(newShape.three)
    originalFour = copy.copy(newShape.four)
    if newShape.name == 'T' or newShape.name == 'S' or newShape.name == 'Z' or newShape.name == 'J' or newShape.name == 'L':
        if not detectCollision(None): #test 1, no kick
            return True #succes, no need to attempt kicks
        wallKickLUT[str([newShape.rotation, 2])]() #test 2
        if not detectCollision(None):
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        wallKickLUT[str([newShape.rotation, 3])][0](), wallKickLUT[str([newShape.rotation, 3])][1]() #test 3
        if not detectCollision(None):
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        wallKickLUT[str([newShape.rotation, 4])][0](), wallKickLUT[str([newShape.rotation, 4])][1]() #test 4
        if not detectCollision(None):
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        wallKickLUT[str([newShape.rotation, 5])][0](), wallKickLUT[str([newShape.rotation, 5])][1](), wallKickLUT[str([newShape.rotation, 5])][2]() #test 5
        if not detectCollision(None):
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset position to before kick
            return False #failure

    if newShape.name == 'I':
        if not detectCollision(None): #test 1, no kick
            return True #succes, no need to attempt kicks
        wallKickLUT_I[str([newShape.rotation, 2])][0](), wallKickLUT_I[str([newShape.rotation, 2])][1]() #test 2
        if not detectCollision(None):
            print("test 2 success")
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        wallKickLUT_I[str([newShape.rotation, 3])][0](), wallKickLUT_I[str([newShape.rotation, 3])][1]() #test 3
        if not detectCollision(None):
            print("test 3 success")
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        wallKickLUT_I[str([newShape.rotation, 4])][0](), wallKickLUT_I[str([newShape.rotation, 4])][1](), wallKickLUT_I[str([newShape.rotation, 4])][2]() #test 4
        if not detectCollision(None):
            print("test 4 success")
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        wallKickLUT_I[str([newShape.rotation, 5])][0](), wallKickLUT_I[str([newShape.rotation, 5])][1](), wallKickLUT_I[str([newShape.rotation, 5])][2]() #test 5
        if not detectCollision(None):
            print("test 5 success")
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset position to before kick
            print("failed")
            return False #failure

def wallKick180():
    global newShape
    originalOne = copy.copy(newShape.one)
    originalTwo = copy.copy(newShape.two)
    originalThree = copy.copy(newShape.three)
    originalFour = copy.copy(newShape.four)
    if not detectCollision(None): #test 1, no kick
        return True #succes, no need to attempt kicks
    wallKickLUT_180[str([newShape.rotation, 2])]() #test 2
    if not detectCollision(None):
        return True #success
    else:
        newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
    wallKickLUT_180[str([newShape.rotation, 3])][0](), wallKickLUT_180[str([newShape.rotation, 3])][1](), wallKickLUT_180[str([newShape.rotation, 3])][2]() #test 3
    if not detectCollision(None):
        return True #success
    else:
        newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
    wallKickLUT_180[str([newShape.rotation, 4])][0](), wallKickLUT_180[str([newShape.rotation, 4])][1]() #test 4
    if not detectCollision(None):
        return True #success
    else:
        newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
    wallKickLUT_180[str([newShape.rotation, 5])][0](), wallKickLUT_180[str([newShape.rotation, 5])][1]() #test 5
    if not detectCollision(None):
        return True #success
    else:
        newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
    wallKickLUT_180[str([newShape.rotation, 6])]() #test 6
    if not detectCollision(None):
        return True #success
    else:
        newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        return False #failed

def moveHorizontal():
    global newShape, dx, lastMove
    if dx == 0:
        return
    if dx < 0 and not touchingExisting_left() and not touchingLeft():
        lastMove = "move left"
        newShape.one.x += dx
        newShape.two.x += dx
        newShape.three.x += dx
        newShape.four.x += dx
    if dx > 0 and not touchingExisting_right() and not touchingRight():
        lastMove = "move right"
        newShape.one.x += dx
        newShape.two.x += dx
        newShape.three.x += dx
        newShape.four.x += dx
    
def touchingExisting_bottom(piece):
    if piece:
        moveDown()
        if placedPiece:
            for i in placedPiece:
                if type(i) is list:
                    continue
                elif piece.colliderect(i):
                    moveUp()
                    return True
            moveUp(); return False
        else: moveUp(); return False

    moveDown()
    if placedPiece:
        for i in placedPiece:
            if type(i) is list:
                continue
            elif newShape.one.colliderect(i) or newShape.two.colliderect(i) or newShape.three.colliderect(i) or newShape.four.colliderect(i):
                moveUp()
                return True
    moveUp()

def touchingExisting_left():
    moveLeft()
    if placedPiece:
        for i in placedPiece:
            if type(i) is list:
                continue
            elif newShape.one.colliderect(i) or newShape.two.colliderect(i) or newShape.three.colliderect(i) or newShape.four.colliderect(i):
                moveRight()
                return True
    moveRight()

def touchingExisting_right():
    moveRight()
    if placedPiece:
        for i in placedPiece:
            if type(i) is list:
                continue
            elif newShape.one.colliderect(i) or newShape.two.colliderect(i) or newShape.three.colliderect(i) or newShape.four.colliderect(i):
                moveLeft()
                return True
    moveLeft()

def touchingLeft():
    moveLeft()
    if newShape.one.colliderect(left) or newShape.two.colliderect(left) or newShape.three.colliderect(left) or newShape.four.colliderect(left):
        moveRight()
        return True
    else: moveRight(); return False

def touchingRight():
    moveRight()
    if newShape.one.colliderect(right) or newShape.two.colliderect(right) or newShape.three.colliderect(right) or newShape.four.colliderect(right):
        moveLeft()
        return True
    else: moveLeft(); return False

def touchingBottom(piece):
    if piece:
        moveDown()
        if piece.colliderect(bottom):
            moveUp()
            return True
        else: moveUp(); return False
    moveDown()
    if newShape.one.colliderect(bottom) or newShape.two.colliderect(bottom) or newShape.three.colliderect(bottom) or newShape.four.colliderect(bottom):
        moveUp()
        return True
    else: moveUp(); return False

def detectCollision(piece): #i messed up here, this is a last min fix
    #for current piece collision use param 0 or None
    if piece: #collision detection for a specific piece 
        if piece.colliderect(bottom) or piece.colliderect(left) or piece.colliderect(right):
            return True
        if placedPiece:
            for i in placedPiece:
                if type(i) is list:
                    continue
                elif piece.colliderect(i):
                    return True
            return False
        else: return False

    if newShape.one.colliderect(bottom) or newShape.two.colliderect(bottom) or newShape.three.colliderect(bottom) or newShape.four.colliderect(bottom):
        return True
    if newShape.one.colliderect(left) or newShape.two.colliderect(left) or newShape.three.colliderect(left) or newShape.four.colliderect(left) or newShape.one.colliderect(right) or newShape.two.colliderect(right) or newShape.three.colliderect(right) or newShape.four.colliderect(right):
        return True
    if placedPiece:
        for i in placedPiece:
            if type(i) is list:
                continue
            elif newShape.one.colliderect(i) or newShape.two.colliderect(i) or newShape.three.colliderect(i) or newShape.four.colliderect(i):
                return True
    else: return False

def resetPiece():
    global newShape
    newShape.rotation = [0, 0]
    if newShape.name == 'O':
        newShape.one = pygame.Rect(420, 210, 30, 30)
        newShape.two = pygame.Rect(450, 210, 30, 30)
        newShape.three = pygame.Rect(450, 240, 30, 30)
        newShape.four = pygame.Rect(420, 240, 30, 30)
    elif newShape.name == 'I':
        newShape.one = pygame.Rect(390, 240, 30, 30)
        newShape.two = pygame.Rect(420, 240, 30, 30)
        newShape.three = pygame.Rect(450, 240, 30, 30)
        newShape.four = pygame.Rect(480, 240, 30, 30)
    elif newShape.name == 'T':
        newShape.one = pygame.Rect(420, 210, 30, 30)
        newShape.two = pygame.Rect(390, 240, 30, 30)
        newShape.three = pygame.Rect(420, 240, 30, 30)
        newShape.four = pygame.Rect(450, 240, 30, 30)
    elif newShape.name == 'S':
        newShape.one = pygame.Rect(420, 210, 30, 30)
        newShape.two = pygame.Rect(450, 210, 30, 30)
        newShape.three = pygame.Rect(390, 240, 30, 30)
        newShape.four = pygame.Rect(420, 240, 30, 30)
    elif newShape.name == 'Z':
        newShape.one = pygame.Rect(390, 210, 30, 30)
        newShape.two = pygame.Rect(420, 210, 30, 30)
        newShape.three = pygame.Rect(420, 240, 30, 30)
        newShape.four = pygame.Rect(450, 240, 30, 30)
    elif newShape.name == 'J':
        newShape.one = pygame.Rect(390, 210, 30, 30)
        newShape.two = pygame.Rect(390, 240, 30, 30)
        newShape.three = pygame.Rect(420, 240, 30, 30)
        newShape.four = pygame.Rect(450, 240, 30, 30)
    elif newShape.name == 'L':
        newShape.one = pygame.Rect(390, 240, 30, 30)
        newShape.two = pygame.Rect(420, 240, 30, 30)
        newShape.three = pygame.Rect(450, 240, 30, 30)
        newShape.four = pygame.Rect(450, 210, 30, 30)

def setPiece():
    global placedPiece, newShape, finishedDropping
    placedPiece.append(newShape.color)
    placedPiece.append(newShape.one)
    placedPiece.append(newShape.two)
    placedPiece.append(newShape.three)
    placedPiece.append(newShape.four)
    resetPiece()
    finishedDropping = True

def drawPastShape():
    for i in placedPiece:
        if type(i) is list:
            color = i
        else: 
            pygame.draw.rect(screen, color, i)

def dropPredict():
    global newShape, placedPiece
    One = copy.copy(newShape.one)
    Two = copy.copy(newShape.two)
    Three = copy.copy(newShape.three)
    Four = copy.copy(newShape.four)
    hitBottom = False
    while hitBottom == False:
        One.y += 30
        Two.y += 30
        Three.y += 30
        Four.y += 30
        if placedPiece:
            for i in placedPiece:
                if type(i) is list:
                    continue
                elif One.colliderect(i) or Two.colliderect(i) or Three.colliderect(i) or Four.colliderect(i):
                    hitBottom = True
                    break
        if One.colliderect(bottom) or Two.colliderect(bottom) or Three.colliderect(bottom) or Four.colliderect(bottom):
            hitBottom = True
    One.y -= 30
    Two.y -= 30
    Three.y -= 30
    Four.y -= 30
    if newShape.name == 'O':
        pygame.draw.rect(screen, (255, 255, 155), One)
        pygame.draw.rect(screen, (255, 255, 155), Two)
        pygame.draw.rect(screen, (255, 255, 155), Three)
        pygame.draw.rect(screen, (255, 255, 155), Four)
    elif newShape.name == 'I':
        pygame.draw.rect(screen, (155, 255, 255), One)
        pygame.draw.rect(screen, (155, 255, 255), Two)
        pygame.draw.rect(screen, (155, 255, 255), Three)
        pygame.draw.rect(screen, (155, 255, 255), Four)
    elif newShape.name == 'T':
        pygame.draw.rect(screen, (128, 64, 128), One)
        pygame.draw.rect(screen, (128, 64, 128), Two)
        pygame.draw.rect(screen, (128, 64, 128), Three)
        pygame.draw.rect(screen, (128, 64, 128), Four)
    elif newShape.name == 'S':
        pygame.draw.rect(screen, (128, 255, 128), One)
        pygame.draw.rect(screen, (128, 255, 128), Two)
        pygame.draw.rect(screen, (128, 255, 128), Three)
        pygame.draw.rect(screen, (128, 255, 128), Four)
    elif newShape.name == 'Z':
        pygame.draw.rect(screen, (255, 128, 128), One)
        pygame.draw.rect(screen, (255, 128, 128), Two)
        pygame.draw.rect(screen, (255, 128, 128), Three)
        pygame.draw.rect(screen, (255, 128, 128), Four)
    elif newShape.name == 'J':
        pygame.draw.rect(screen, (128, 128, 255), One)
        pygame.draw.rect(screen, (128, 128, 255), Two)
        pygame.draw.rect(screen, (128, 128, 255), Three)
        pygame.draw.rect(screen, (128, 128, 255), Four)
    elif newShape.name == 'L':
        pygame.draw.rect(screen, (255, 192, 128), One)
        pygame.draw.rect(screen, (255, 192, 128), Two)
        pygame.draw.rect(screen, (255, 192, 128), Three)
        pygame.draw.rect(screen, (255, 192, 128), Four)

def lineClear():
    global placedPiece
    yValues = [] #list of all the placed pieces' y coordinates
    fullLines = [] #list of all full lines
    for i in placedPiece:
        if type(i) is list: 
            continue
        else: 
            yValues.append(i.y) #add the y coordinates to the list
    for y in range(300, 900, 30):
        if yValues.count(y) == 10:
            fullLines.append(y) #if there are more than 10 tiles on the same y levels it is a full line
    if not fullLines: 
        return #quit if there aren't any full lines
    print(fullLines)

    i = 0
    while i < len(placedPiece): #remove the full lines
        if type(placedPiece[i]) is list:
            i += 1
            continue
        elif not placedPiece[i].y in fullLines:
            i += 1
        elif placedPiece[i].y in fullLines:
            placedPiece.pop(i)


    t1 = mt.Thread(target=generateParticles, args=(fullLines, None, WHITE, 0.5, round(6.5-1.4*len(fullLines)),))
    t2 = mt.Thread(target=fallDown, args=(fullLines,))

    t1.start()
    t2.start()

    t2.join()
    t1.join()

def fallDown(lines):
    global placedPiece
    for h in lines: #move the remaining pieces down
        for i in placedPiece: 
            if type(i) is list:
                continue
            if i.y < h: 
                i.y += 30

def checkTspin():
    global newShape, lastMove
    a = pygame.Rect(newShape.three.x - 30, newShape.three.y - 30, 30, 30)
    b = pygame.Rect(newShape.three.x + 30, newShape.three.y - 30, 30, 30)
    c = pygame.Rect(newShape.three.x - 30, newShape.three.y + 30, 30, 30)
    d = pygame.Rect(newShape.three.x + 30, newShape.three.y + 30, 30, 30)
    
    if lastMove == "rotation" and ((detectCollision(a) + detectCollision(b) + detectCollision(c) + detectCollision(d)) >= 3) and newShape.three.y - yCoordinate == 0: 
        print("t spin!")

def checkPC():
    global placedPiece
    for i in placedPiece:
        if type(i) is pygame.Rect:
            return False
    print("PERFECT CLEAR!")
    return True


def hardDrop():
    while not touchingBottom(None) and not touchingExisting_bottom(None):
        moveDown()
        drawShape()
        pygame.display.update()
        pygame.time.delay(1)
    if newShape.name == 'T':
        checkTspin()

def hardDrop2():
    global pieceCount
    setPiece()
    pieceCount += 1
    lineClear()
    checkPC()



pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("aw lord")
screen = pygame.display.set_mode((900, 1000), flags=pygame.RESIZABLE) 
bottom = pygame.Rect(300, 900, 300, 300)
left = pygame.Rect(0, 0, 300, 1000)
right = pygame.Rect(600, 0, 300, 1000)

GREY = (71, 71, 71)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
run = True

dx, softDrop = 0, False
placedPiece = list()
bag = list()
queue = []
holdPiece = None
holdLock = False
input = bool()
dropped = False
finishedDropping = True
pieceCount = 0
frameCount = 0
droppedTime = int()
lastMove = str()
yCoordinate = 0


screen.fill(BLACK)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN: #has to be inside the for loop 
            if event.key == pygame.K_DOWN: #down
                softDrop = True
                input = True
            if event.key == pygame.K_LEFT: #left
                dx = -30
                input = True
            if event.key == pygame.K_RIGHT: #right
                dx = 30
                input = True 
            if event.key == pygame.K_SPACE: #hard drop
                hardDrop()
                #hardDropParticles()
                hardDrop2()
            if event.key == pygame.K_ESCAPE: #quit
                run = False
            if event.key == pygame.K_z: #rotate CCW
                rotateCCW()
                input = True
            if event.key == pygame.K_x: #rotate CW
                rotateCW()
                input = True
            if event.key == pygame.K_a: #rotate 180
                rotate180()
                input = True
            if event.key == pygame.K_c: #hold
                hold()
        if event.type == pygame.KEYUP: #stop
            if event.key == pygame.K_DOWN:
                softDrop = False
                input = False
            if event.key == pygame.K_LEFT:
                dx = 0
                input = False
            if event.key == pygame.K_RIGHT:
                dx = 0
                input = False
            if event.key == pygame.K_z:
                input = False
            if event.key == pygame.K_x:
                input = False
            if event.key == pygame.K_a:
                input = False
    #-----^^INPUT CHECK^^-----#
    frameCount += 1

    if finishedDropping == True: #if previous piece has been dropped
        newPiece()
        finishedDropping = False

    if softDrop == True and dropped == False and not touchingBottom(None) and not touchingExisting_bottom(None) and frameCount %2 == 0: #if softdrop is inputted
        lastMove = "move down"
        moveDown()
    if frameCount %2 == 0:
        moveHorizontal() #check if it needs to be shifted horizontally and does so

    if frameCount % 8 == 0 and input == False and dropped == False and not frameCount % 24 == 0: #move down every 12 frames
        moveDown()
    if frameCount % 24 == 0 and dropped == False and softDrop == False: #prevent player from stalling game by holding rotate/move by force moving every 12 frames
        moveDown()

    checkDropped() #check if this piece has been dropped
  
    #print(dropped)
    #print(frameCount - droppedTime)
    if dropped == True and frameCount - droppedTime >= 15: 
        print("hard drop")
        hardDrop()  
        hardDrop2()

    #-----\UPDATE DISPLAY/-----#
    
    screen.fill(BLACK) #fill in the black background
    dropPredict() #update the drop predict
    drawShape() #draw the urrent piece after the shifts
    drawPastShape() #draw all the previously dropped pieces
    #pygame.draw.rect(screen, [255, 0, 255], bottom)
    drawGrid()
    pygame.draw.line(screen, WHITE, (300, 300), (300, 900), 5)
    pygame.draw.line(screen, WHITE, (298, 900), (602, 900), 5)
    pygame.draw.line(screen, WHITE, (600, 300), (600, 900), 5)
    pygame.display.update()
    #print(dropped)


    

    clock.tick(30) #15 FPS

pygame.quit()  # de-initialize the pygame module
print(pieceCount)


