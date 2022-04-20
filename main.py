from hashlib import new
import pygame
import random
import copy

def drawGrid(): 
    blockSize = 30 #Set the size of the grid block
    for x in range(300, 600, blockSize):
        for y in range(300, 900, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, GREY, rect, 1)

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
        if not touchingBottom() and not touchingExisting_bottom():
            print("e")
            dropped = False
            droppedTime = 0
    elif touchingBottom() or touchingExisting_bottom():
        dropped = True
        droppedTime = frameCount
        return

def newPiece():
    global newShape, pieceCount, bag, dropped
    if pieceCount % 7 == 0:
        bag = [O, I, T, J, L, S , Z]
    newShape = random.choice(bag)
    bag.remove(newShape)
    dropped = False

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
    originalOne = copy.copy(newShape.one)
    originalTwo = copy.copy(newShape.two)
    originalThree = copy.copy(newShape.three)
    originalFour = copy.copy(newShape.four)
    originalRotation = copy.copy(newShape.rotation)
    if newShape.name == 'O':
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
            else: return
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
            else: return
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
            else: return
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
            else: return

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
            else: return
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
            else: return
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
            else: return
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
            else: return
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
            else: return
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
            else: return
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
            else: return
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
            else: return

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
            else: return
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
            else: return
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
            else: return
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
            else: return

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
            else: return
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
            else: return
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
            else: return
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
            else: return

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
            else: return
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
            else: return
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
            else: return
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
            else: return

def rotateCW():
    global newShape
    originalOne = copy.copy(newShape.one)
    originalTwo = copy.copy(newShape.two)
    originalThree = copy.copy(newShape.three)
    originalFour = copy.copy(newShape.four)
    originalRotation = copy.copy(newShape.rotation)
    if newShape.name == 'O':
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
            else: return
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
            else: return
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
            else: return
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
            else: return
    
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
            else: return
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
            else: return
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
            else: return
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
            else: return

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
            else: return
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
            else: return
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
            else: return
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
            else: return

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
            else: return
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
            else: return
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
            else: return
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
            else: return

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
            else: return
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
            else: return
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
            else: return
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
            else: return
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
            else: return
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
            else: return
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
            else: return
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
            else: return

def rotate180():
    global newShape
    originalOne = copy.copy(newShape.one)
    originalTwo = copy.copy(newShape.two)
    originalThree = copy.copy(newShape.three)
    originalFour = copy.copy(newShape.four)
    originalRotation = copy.copy(newShape.rotation)
    if newShape.name == 'O':
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
            else: return
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
            else: return
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
            else: return
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
            else: return

    elif newShape.name == 'T':
        if newShape.rotation[1] == 0: #rotation 0 to 2
            newShape.one.y += 60
            newShape.two.x += 60
            newShape.four.x -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return
        elif newShape.rotation[1] == 1: #roation 1 to 3
            newShape.one.x -= 60
            newShape.two.y += 60
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return
        elif newShape.rotation[1] == 2: #rotation 2 to 0
            newShape.one.y -= 60
            newShape.two.x -= 60
            newShape.four.x += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return
        elif newShape.rotation[1] == 3: #rotation 3 to 1
            newShape.one.x += 60
            newShape.two.y -= 60
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return

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
            else: return
        elif newShape.rotation[1] == 1: #rotation 1 to 3
            newShape.one.x -= 60
            newShape.one.y += 60
            newShape.two.y += 60
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return
        elif newShape.rotation[1] == 2: #rotation 2 to 0
            newShape.one.x -= 60
            newShape.one.y -= 60
            newShape.two.x -= 60
            newShape.four.x += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return
        elif newShape.rotation[1] == 3: #rotation 3 to 1
            newShape.one.x += 60
            newShape.one.y -= 60
            newShape.two.y -= 60
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return

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
            else: return
        elif newShape.rotation[1] == 1: #rotation 1 to 3
            newShape.one.y += 60
            newShape.three.y -= 60
            newShape.four.x -= 60
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return
        elif newShape.rotation[1] == 2: #rotation 2 to 0
            newShape.one.x -= 60
            newShape.three.x += 60
            newShape.four.x += 60
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return
        elif newShape.rotation[1] == 3: #rotation 3 to 1
            newShape.one.y -= 60
            newShape.three.y += 60
            newShape.four.x += 60
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return

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
            else: return
        elif newShape.rotation[1] == 1: #rotation 1 to 3
            newShape.one.x -= 60
            newShape.two.x -= 60
            newShape.two.y -= 60
            newShape.three.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return
        elif newShape.rotation[1] == 2: #rotation 2 to 0
            newShape.one.y -= 60
            newShape.two.x += 60
            newShape.two.y -= 60
            newShape.three.x -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return
        elif newShape.rotation[1] == 3: #rotation 3 to 1
            newShape.one.x += 60
            newShape.two.x += 60
            newShape.two.y += 60
            newShape.three.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return
    
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
            else: return
        elif newShape.rotation[1] == 1: #rotation 1 to 3
            newShape.one.x -= 60
            newShape.one.y += 60
            newShape.two.x -= 60
            newShape.four.y -= 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return
        elif newShape.rotation[1] == 2: #rotation 2 to 0
            newShape.one.x -= 60
            newShape.one.y -= 60
            newShape.two.y -= 60
            newShape.four.x += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return
        elif newShape.rotation[1] == 3: #rotation 3 to 1
            newShape.one.x += 60
            newShape.one.y -= 60
            newShape.two.x += 60
            newShape.four.y += 60
            newShape.rotation[0] = newShape.rotation[1] #shift the previous current rotation index to past tense
            newShape.rotation[1] = (newShape.rotation[0]+2)%4 #update current rotation index
            if not wallKick180(): #rotation is possible, undo everything
                newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour); newShape.rotation = copy.copy(originalRotation)
            else: return

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
        if not detectCollision(): #test 1, no kick
            return True #succes, no need to attempt kicks
        wallKickLUT[str([newShape.rotation, 2])]() #test 2
        if not detectCollision():
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        wallKickLUT[str([newShape.rotation, 3])][0](), wallKickLUT[str([newShape.rotation, 3])][1]() #test 3
        if not detectCollision():
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        wallKickLUT[str([newShape.rotation, 4])][0](), wallKickLUT[str([newShape.rotation, 4])][1]() #test 4
        if not detectCollision():
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        wallKickLUT[str([newShape.rotation, 5])][0](), wallKickLUT[str([newShape.rotation, 5])][1](), wallKickLUT[str([newShape.rotation, 5])][2]() #test 5
        if not detectCollision():
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset position to before kick
            return False #failure

    if newShape.name == 'I':
        if not detectCollision(): #test 1, no kick
            return True #succes, no need to attempt kicks
        wallKickLUT_I[str([newShape.rotation, 2])][0](), wallKickLUT_I[str([newShape.rotation, 2])][1]() #test 2
        if not detectCollision():
            print("test 2 success")
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        wallKickLUT_I[str([newShape.rotation, 3])][0](), wallKickLUT_I[str([newShape.rotation, 3])][1]() #test 3
        if not detectCollision():
            print("test 3 success")
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        wallKickLUT_I[str([newShape.rotation, 4])][0](), wallKickLUT_I[str([newShape.rotation, 4])][1](), wallKickLUT_I[str([newShape.rotation, 4])][2]() #test 4
        if not detectCollision():
            print("test 4 success")
            return True #success
        else:
            newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        wallKickLUT_I[str([newShape.rotation, 5])][0](), wallKickLUT_I[str([newShape.rotation, 5])][1](), wallKickLUT_I[str([newShape.rotation, 5])][2]() #test 5
        if not detectCollision():
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
    if not detectCollision(): #test 1, no kick
        return True #succes, no need to attempt kicks
    wallKickLUT_180[str([newShape.rotation, 2])]() #test 2
    if not detectCollision():
        return True #success
    else:
        newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
    wallKickLUT_180[str([newShape.rotation, 3])][0](), wallKickLUT_180[str([newShape.rotation, 3])][1](), wallKickLUT_180[str([newShape.rotation, 3])][2]() #test 3
    if not detectCollision():
        return True #success
    else:
        newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
    wallKickLUT_180[str([newShape.rotation, 4])][0](), wallKickLUT_180[str([newShape.rotation, 4])][1]() #test 4
    if not detectCollision():
        return True #success
    else:
        newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
    wallKickLUT_180[str([newShape.rotation, 5])][0](), wallKickLUT_180[str([newShape.rotation, 5])][1]() #test 5
    if not detectCollision():
        return True #success
    else:
        newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
    wallKickLUT_180[str([newShape.rotation, 6])]() #test 6
    if not detectCollision():
        return True #success
    else:
        newShape.one = copy.copy(originalOne); newShape.two = copy.copy(originalTwo); newShape.three = copy.copy(originalThree); newShape.four = copy.copy(originalFour) #reset the position for next test
        return False #failed

def moveHorizontal():
    global newShape, deltaX
    if deltaX == 0:
        return
    if deltaX < 0 and not touchingExisting_left() and not touchingLeft():
        newShape.one.x += deltaX
        newShape.two.x += deltaX
        newShape.three.x += deltaX
        newShape.four.x += deltaX
    if deltaX > 0 and not touchingExisting_right() and not touchingRight():
        newShape.one.x += deltaX
        newShape.two.x += deltaX
        newShape.three.x += deltaX
        newShape.four.x += deltaX
    
def touchingExisting_bottom():
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

def touchingBottom():
    moveDown()
    if newShape.one.colliderect(bottom) or newShape.two.colliderect(bottom) or newShape.three.colliderect(bottom) or newShape.four.colliderect(bottom):
        moveUp()
        return True
    else: moveUp(); return False

def detectCollision():
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

def hardDrop():
    global pieceCount
    while not touchingBottom() and not touchingExisting_bottom():
        moveDown()
        drawShape()
        pygame.display.update()
        pygame.time.delay(1)
    setPiece()
    pieceCount += 1

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("aw lord")
screen = pygame.display.set_mode((900, 1000)) 
bottom = pygame.Rect(300, 900, 300, 300)
left = pygame.Rect(0, 0, 300, 1000)
right = pygame.Rect(600, 0, 300, 1000)

GREY = (71, 71, 71)
BLACK = (0,0,0)
run = True

deltaX, softDrop = 0, False
placedPiece = list()
bag = list()
input = bool()
dropped = False
finishedDropping = True
pieceCount = 0
frameCount = 0
droppedTime = int()


screen.fill(BLACK)
while run:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: #has to be inside the for loop 
            if event.key == pygame.K_DOWN: #down
                softDrop = True
                input = True
            if event.key == pygame.K_LEFT: #left
                deltaX = -30
                input = True
            if event.key == pygame.K_RIGHT: #right
                deltaX = 30
                input = True 
            if event.key == pygame.K_SPACE:
                hardDrop()
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_z:
                rotateCCW()
                input = True
            if event.key == pygame.K_x:
                rotateCW()
                input = True
            if event.key == pygame.K_a:
                rotate180()
                input = True
        if event.type == pygame.KEYUP: #stop
            if event.key == pygame.K_DOWN:
                softDrop = False
                input = False
            if event.key == pygame.K_LEFT:
                deltaX = 0
                input = False
            if event.key == pygame.K_RIGHT:
                deltaX = 0
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

    if softDrop == True and dropped == False and not touchingBottom() and not touchingExisting_bottom(): #if softdrop is inputted
        moveDown()

    moveHorizontal() #check if it needs to be shifted horizontally and does so

    if frameCount % 4 == 0 and input == False and dropped == False and not frameCount % 12 == 0: #move down every 12 frames
        moveDown()
    if frameCount % 12 == 0 and dropped == False and softDrop == False: #prevent player from stalling game by holding rotate/move by force moving every 12 frames
        moveDown()

    checkDropped() #check if this piece has been dropped
  
    #print(dropped)
    #print(frameCount - droppedTime)
    if dropped == True and frameCount - droppedTime >= 15: 
        print("hard drop")
        hardDrop()  

    #-----\UPDATE DISPLAY/-----#
    
    screen.fill(BLACK) #fill in the black background
    dropPredict() #update the drop predict
    drawShape() #draw the urrent piece after the shifts
    drawPastShape() #draw all the previously dropped pieces
    pygame.draw.rect(screen, [255, 0, 255], bottom)
    drawGrid()
    detectCollision()
    pygame.display.update()
    #print(dropped)


    

    clock.tick(15) #15 FPS

pygame.quit()  # de-initialize the pygame module
print(pieceCount)


