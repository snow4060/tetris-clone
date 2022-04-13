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
    color = [255, 255, 0] #yellow
    name = 'O'

class I:
    one = pygame.Rect(390, 240, 30, 30)
    two = pygame.Rect(420, 240, 30, 30)
    three = pygame.Rect(450, 240, 30, 30)
    four = pygame.Rect(480, 240, 30, 30)
    color = [0, 255, 255] #cyan 
    name = 'I'

def drawShape():
    pygame.draw.rect(screen, newShape.color, newShape.one)
    pygame.draw.rect(screen, newShape.color, newShape.two)
    pygame.draw.rect(screen, newShape.color, newShape.three)
    pygame.draw.rect(screen, newShape.color, newShape.four)
    
def checkDropped():
    global dropped, pieceCount, newShape, frameCount, droppedTime, placedPiece
    if newShape.one.colliderect(bottom) or newShape.two.colliderect(bottom) or newShape.three.colliderect(bottom) or newShape.four.colliderect(bottom):
        moveUp()
        dropped = True
        droppedTime = frameCount
        return
    if placedPiece:
        for i in placedPiece:
            if type(i) is list:
                continue
            elif newShape.one.colliderect(i) or newShape.two.colliderect(i) or newShape.three.colliderect(i) or newShape.four.colliderect(i):
                moveUp()
                dropped = True
                droppedTime = frameCount
                return

def newPiece():
    global newShape, pieceCount, bag, piece, dropped
    if pieceCount % 2 == 0:
        bag = ['O', 'I']
    piece = random.choice(bag)
    if piece == 'O':
        newShape = O
        bag.remove('O')
    if piece == 'I':
        newShape = I
        bag.remove('I')
    pieceCount += 1
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

def moveHorizontal():
    global left, right, newShape, deltaX
    if deltaX == 0:
        return
    newShape.one.x += deltaX
    newShape.two.x += deltaX
    newShape.three.x += deltaX
    newShape.four.x += deltaX
    if newShape.one.colliderect(left) or newShape.two.colliderect(left) or newShape.three.colliderect(left) or newShape.four.colliderect(left) or newShape.one.colliderect(right) or newShape.two.colliderect(right) or newShape.three.colliderect(right) or newShape.four.colliderect(right):
        newShape.one.x -= deltaX
        newShape.two.x -= deltaX
        newShape.three.x -= deltaX
        newShape.four.x -= deltaX
    


def resetPiece():
    global newShape
    if newShape.name == 'O':
        newShape.one = pygame.Rect(420, 210, 30, 30)
        newShape.two = pygame.Rect(450, 210, 30, 30)
        newShape.three = pygame.Rect(450, 240, 30, 30)
        newShape.four = pygame.Rect(420, 240, 30, 30)
    if newShape.name == 'I':
        newShape.one = pygame.Rect(390, 240, 30, 30)
        newShape.two = pygame.Rect(420, 240, 30, 30)
        newShape.three = pygame.Rect(450, 240, 30, 30)
        newShape.four = pygame.Rect(480, 240, 30, 30)

def setPiece():
    global placedPiece, newShape, hardDropped
    placedPiece.append(newShape.color)
    placedPiece.append(newShape.one)
    placedPiece.append(newShape.two)
    placedPiece.append(newShape.three)
    placedPiece.append(newShape.four)
    resetPiece()
    hardDropped = True

def drawPastShape():
    global placedPiece
    for i in placedPiece:
        if type(i) is list:
            color = i
        else: 
            pygame.draw.rect(screen, color, i)

def dropPredict():
    global newShape, placedPiece, bottom
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
    if newShape.name == 'I':
        pygame.draw.rect(screen, (155, 255, 255), One)
        pygame.draw.rect(screen, (155, 255, 255), Two)
        pygame.draw.rect(screen, (155, 255, 255), Three)
        pygame.draw.rect(screen, (155, 255, 255), Four)
    elif newShape.name == 'O':
        pygame.draw.rect(screen, (255, 255, 155), One)
        pygame.draw.rect(screen, (255, 255, 155), Two)
        pygame.draw.rect(screen, (255, 255, 155), Three)
        pygame.draw.rect(screen, (255, 255, 155), Four)

def hardDrop():
    global newShape, placedPiece, bottom
    hitBottom = False
    while hitBottom == False:
        newShape.one.y += 30
        newShape.two.y += 30
        newShape.three.y += 30
        newShape.four.y += 30
        if placedPiece:
            for i in placedPiece:
                if type(i) is list:
                    continue
                elif newShape.one.colliderect(i) or newShape.two.colliderect(i) or newShape.three.colliderect(i) or newShape.four.colliderect(i):
                    hitBottom = True
                    break
        if newShape.one.colliderect(bottom) or newShape.two.colliderect(bottom) or newShape.three.colliderect(bottom) or newShape.four.colliderect(bottom):
            hitBottom = True
        
    
    newShape.one.y -= 30
    newShape.two.y -= 30
    newShape.three.y -= 30
    newShape.four.y -= 30
    setPiece()

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("aw lord")
screen = pygame.display.set_mode((900, 1000)) 
bottom = pygame.Rect(300, 900, 300, 100)
left = pygame.Rect(0, 0, 300, 1000)
right = pygame.Rect(600, 0, 300, 1000)

GREY = (71, 71, 71)
BLACK = (0,0,0)
run = True

deltaX, deltaY = 0, 0
placedPiece = list()
bag = list()
input = bool()
dropped = True
hardDropped = True
pieceCount = 0
frameCount = 0

screen.fill(BLACK)
while run:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: #has to be inside the for loop 
            if event.key == pygame.K_DOWN: #down
                deltaY = 30
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
        if event.type == pygame.KEYUP: #stop
            if event.key == pygame.K_DOWN:
                deltaY = 0
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

    frameCount += 1

    if hardDropped == True:
        newPiece()
        hardDropped = False

    if not deltaY == 0:
        moveDown()

    moveHorizontal()



    screen.fill(BLACK) #update screen
    #pygame.draw.rect(screen, YELLOW, (x, y, 30, 30))
    dropPredict()
    drawShape()
    drawPastShape()
    checkDropped()

    if frameCount % 4 == 0 and input == False and dropped == False and not frameCount % 12 == 0:
        moveDown()
    if frameCount % 12 == 0 and dropped == False and deltaY == 0: #prevent player from stalling game by holding rotate/move by force moving every 12 frames
        moveDown()
    if dropped == True:
        setPiece()
    drawGrid()
    pygame.display.update()

    clock.tick(20) #20 FPS

pygame.quit()  # de-initialize the pygame module
print(pieceCount)

