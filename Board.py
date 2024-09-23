from random import random as r
import random
from queue import Queue
import numpy as n
import math as m
import pygame
from array import *
from Block import *
from Tetrominoes import *
from GhostTetros import *

# variables:
# queue for the queue of tetrominoes (3)
# reference to tetromino in hold and falling
# 2d vector of blocks



# functions:
# spawn a random block
# tick (the block tries to fall)
# try move (create a new piece and check if it is colliding)
# try rotate (create a new piece and check if it is colliding)
# swap out
# draw

class Board:

    
    

    def __init__(self, screen):
        self.screen = screen

    

    def setup (self):
        
        
        #self.falling = self.spawnRandom()
        #self.shadow = self.spawnShadow()

        self.bag = [I_Block(0, 0), J_Block(0, 0), L_Block(0, 0), O_Block(0, 0), S_Block(0, 0), Z_Block(0, 0), T_Block(0, 0)]
        random.shuffle(self.bag)
        self.queueBag = Queue()

        self.falling = self.bag[0]
        self.shadow = self.spawnShadow()

        match self.falling.name:
            case "I_Piece": 
                self.falling.update_pos(Block.dim * 12, Block.dim * 2)
            case "O_Piece":
                self.falling.update_pos(Block.dim * 12, Block.dim * 2)
            case _:
                self.falling.update_pos(Block.dim * 11, Block.dim * 2)

        self.q = Queue()

        # self.q.put(self.spawnRandom())
        # self.q.put(self.spawnRandom())
        # self.q.put(self.spawnRandom())
        # self.q.put(self.spawnRandom())
        # self.q.put(self.spawnRandom())

        self.holdPiece = None
        self.holdable = True

        self.onGroundBool = [[False for i in range(24)] for j in range (10)]
        self.onGroundBlock = [[None for i in range(24)] for j in range (10)]

        self.ticksTouching = 0

        self.lost = False
        self.won = False

        self.score = 0
        self.scoring = True
        self.linesInLevel = 0

        
        
        self.q.put(self.bag[1])
        self.q.put(self.bag[2])
        self.q.put(self.bag[3])
        self.q.put(self.bag[4])
        self.q.put(self.bag[5])

        self.bagIndex = 6


        self.lines = 0

        self.level = 0

        self.startTime = pygame.time.get_ticks()

    def draw(self):
        
        if not self.lost:

            #hold
            pygame.draw.rect(self.screen, "white", pygame.Rect(Block.dim * 2, Block.dim * 4, Block.dim * 5, Block.dim)) # top block of hold
            pygame.draw.line(self.screen, "white", pygame.Vector2(Block.dim * 2, Block.dim * 5), pygame.Vector2(Block.dim * 2, Block.dim * 8), 2) #left side hold line
            pygame.draw.line(self.screen, "white", pygame.Vector2(Block.dim * 2, Block.dim * 8), pygame.Vector2(Block.dim * 7 - 2, Block.dim * 8), 2) # right

            #main board
            pygame.draw.line(self.screen, "white", pygame.Vector2(Block.dim * 7 - 2, Block.dim * 4), pygame.Vector2(Block.dim * 7 - 2, Block.dim * 24), 2) # left side of board
            pygame.draw.line(self.screen, "white", pygame.Vector2(Block.dim * 7, Block.dim * 24), pygame.Vector2(Block.dim * 17, Block.dim * 24), 2) # bottom
            pygame.draw.line(self.screen, "white", pygame.Vector2(Block.dim * 17, Block.dim * 24), pygame.Vector2(Block.dim * 17, Block.dim * 4), 2) # right

            #queue
            pygame.draw.rect(self.screen, "white", pygame.Rect(Block.dim * 17, Block.dim * 4, Block.dim * 5, Block.dim)) # block
            pygame.draw.line(self.screen, "white", pygame.Vector2(Block.dim * 22 - 2, Block.dim * 5), pygame.Vector2(Block.dim * 22 - 2, Block.dim * 5 + Block.dim * 3 * self.q.qsize()), 2) # right line
            pygame.draw.line(self.screen, "white", pygame.Vector2(Block.dim * 17, Block.dim * 5  + Block.dim * 3 * self.q.qsize()), pygame.Vector2(Block.dim * 22 - 2, Block.dim * 5  + Block.dim * 3 * self.q.qsize()), 2)

            #text
            allFont = pygame.font.Font("freesansbold.ttf", 30)

            holdText = allFont.render('Hold', True, "Black", "White")
            holdRect = holdText.get_rect()
            holdRect.center = (95, 135)
            self.screen.blit(holdText, holdRect)

            qText = allFont.render('Next', True, "Black", "White")
            qRect = qText.get_rect()
            qRect.center = (545, 135)
            self.screen.blit(qText, qRect)

            #time
            timeText = allFont.render('Time: ', True, "White", "gray10")
            timeRect = timeText.get_rect()
            timeRect.center = (570, 630)
            self.screen.blit(timeText, timeRect)

            mins = int((pygame.time.get_ticks() - self.startTime) / 60000)
            secs = (int (m.trunc((pygame.time.get_ticks() - self.startTime) / 1000) % 60))
            decimals = (m.trunc((pygame.time.get_ticks() - self.startTime)/10) % 100)
        
            accTimeText = allFont.render( f"{mins : 03d}:{secs :02d}.{decimals:02d}", True, "White", "gray10")  
                 
            
            accTimeRect = accTimeText.get_rect()
            accTimeRect.center = (590, 670)
            self.screen.blit(accTimeText, accTimeRect)

            #queue pieces
            
            tempQ = Queue()

            for i in range(int(self.q.qsize())):
                piece = self.q.get()
                if piece.name == "I_Piece":
                    piece.update_pos(19 * Block.dim + Block.dim / 2, Block.dim * 7 + Block.dim * 3 * i)
                elif piece.name == "O_Piece":
                    piece.update_pos(19 * Block.dim + Block.dim / 2, Block.dim * 6 + Block.dim / 2 + Block.dim * 3 * i)
                else:
                    piece.update_pos (19 * Block.dim, Block.dim * 6 + Block.dim / 2 + Block.dim * 3 * i)

                piece.draw(self.screen)
                tempQ.put(piece)
            
            self.q = tempQ

            #shadow piece

            self.shadow.update_pos(self.falling.centerX, self.falling.centerY)

            self.dropShadow()

            self.shadow.draw(self.screen)

            #falling piece

            self.falling.draw(self.screen)

            #hold piece
            
            if self.holdPiece != None:
                if self.holdPiece.name == "I_Piece":
                    self.holdPiece.update_pos(4 * Block.dim + Block.dim / 2, Block.dim * 7)
                elif self.holdPiece.name == "O_Piece":
                    self.holdPiece.update_pos(4 * Block.dim + Block.dim / 2, Block.dim * 6 + Block.dim / 2)
                else:
                    self.holdPiece.update_pos (4 * Block.dim, Block.dim * 6 + Block.dim / 2)

                self.holdPiece.draw(self.screen)

            #placed blocks

            for i in range(10):
                for j in range (24):
                    if self.onGroundBool[i][j]:
                        self.onGroundBlock[i][j].update_pos((i + 7) * Block.dim, j * Block.dim)
                        self.onGroundBlock[i][j].draw(self.screen)

            #score text

        
            scoreText = allFont.render('Score:', True, "White", "gray10")
            scoreRect = scoreText.get_rect()
            scoreRect.center = (120, 630)
            self.screen.blit(scoreText, scoreRect)
        
            accTimeText = allFont.render(str(self.score), True, "White", "gray10")
            accTimeRect = accTimeText.get_rect()
            accTimeRect.center = (130, 670)
            self.screen.blit(accTimeText, accTimeRect)

            #lines text

            lineText = allFont.render('Lines: ', True, "White", "gray10")
            lineRect = lineText.get_rect()
            lineRect.center = (120, 530)
            self.screen.blit(lineText, lineRect)

            linesText = allFont.render(str(self.lines) + "/40", True, "White", "gray10")
            linesRect = linesText.get_rect()
            linesRect.center = (120, 570)
            self.screen.blit(linesText, linesRect)

            #level text

            lvlText = allFont.render("Level " + str(self.level), True, "White", "gray10")
            lvlRect = lvlText.get_rect()
            lvlRect.center = (120, 430)
            self.screen.blit(lvlText, lvlRect)





        else:
           # lose screen
            generalFont = pygame.font.Font("freesansbold.ttf", 30)
            bigFont = pygame.font.Font("freesansbold.ttf", 40)

            loseText = bigFont.render("You Lost!", True, "red", "gray10")
            loseRect = loseText.get_rect()
            loseRect.center = (360, 370)
            self.screen.blit(loseText, loseRect)

            restartText = bigFont.render("Press [R] to restart", True, "white", "gray10")
            restartRect = restartText.get_rect()
            restartRect.center = (360, 410)
            self.screen.blit(restartText, restartRect)

            scoreText = generalFont.render("Score: " + str(self.score), True, "white", "gray10")
            scoreRect = scoreText.get_rect()
            scoreRect.center = (220, 470)
            self.screen.blit(scoreText, scoreRect)

            lineText = generalFont.render("Lines: " + str(self.lines), True, "white", "gray10")
            lineRect = lineText.get_rect()
            lineRect.center = (500, 470)
            self.screen.blit(lineText, lineRect)




    
# game functions

    def place(self):
        blocks = self.falling.return_blocks()

        y_values = []
        
        for block in blocks: #add the blocks to the array
            self.onGroundBlock[int(block.x / Block.dim) - 7][int(block.y / Block.dim)] = block
            self.onGroundBool[int(block.x / Block.dim) - 7][int(block.y / Block.dim)] = True

            y_values.append(int (block.y / Block.dim))

        y_values = list(dict.fromkeys(y_values))

        y_values = sorted(y_values)

        cleared = 0

        for y in y_values:
            if (self.checkLine(y)):
                cleared += 1
            if (y < 3):
                self.lost = True
                

        self.updateScore(cleared)
        self.lines += cleared

        self.linesInLevel += cleared
        self.updateLvl()

        #change the falling block and add a random block to queue
        self.falling = self.q.get()
        
        match self.falling.name:
            case "I_Piece": 
                self.falling.update_pos(Block.dim * 12, Block.dim * 2)
            case "O_Piece":
                self.falling.update_pos(Block.dim * 12, Block.dim * 2)
            case _:
                self.falling.update_pos(Block.dim * 11, Block.dim * 2)

        self.spawnfrom7bag()

        self.shadow = self.spawnShadow()

        self.holdable = True

    def hold(self):
        if self.holdable:
            if self.holdPiece != None:
                temp = self.holdPiece
            else:
                temp = self.q.get()
                self.spawnfrom7bag()

            match self.falling.name:
                case "I_Piece":
                    self.holdPiece = I_Block(0, 0)
                case "O_Piece":
                    self.holdPiece = O_Block(0, 0)
                case "J_Piece":
                    self.holdPiece = J_Block(0, 0)
                case "L_Piece":
                    self.holdPiece = L_Block(0, 0)
                case "T_Piece":
                    self.holdPiece = T_Block(0, 0)
                case "S_Piece":
                    self.holdPiece = S_Block(0, 0)
                case "Z_Piece":
                    self.holdPiece = Z_Block(0, 0)


            self.falling = temp

            match self.falling.name:
                case "I_Piece": 
                    self.falling.update_pos(Block.dim * 12, Block.dim * 2)
                case "O_Piece":
                    self.falling.update_pos(Block.dim * 12, Block.dim * 2)
                case _:
                    self.falling.update_pos(Block.dim * 11, Block.dim * 2)
            self.holdable = False

            self.shadow = self.spawnShadow()
        
    def hardDrop(self):
        while (not self.checkBelow(self.falling)):
            self.falling.fall()
        
        self.falling.update_pos(self.falling.centerX, self.falling.centerY - Block.dim)

        self.place()
    
    def updateScore(self, lines):
        if lines == 0:
            return
        if lines == 1:
            self.score += 4 * (self.level + 1)
        if lines == 2:
            self.score += 10 * (self.level + 1)
        if lines == 3:
            self.score += 30 * (self.level + 1)
        if lines == 4:
            self.score += 120 * (self.level + 1)

    def updateLvl(self): #when the lvlscore is at a certain threshold, (maybe 5k, 10k, then 20k) (5k = lvls 1-10, 10k = lvls 11-20, 20k = lvls 21+), increase the level by one
        if (self.linesInLevel >= self.level * 10 + 10) or (self.linesInLevel >= max(100, self.level * 10 - 50)):
            self.linesInLevel = 0
            self.level += 1

        

# movement

    def tryMove(self, tetromino, input):
        prevCenterX = tetromino.centerX
        prevCenterY = tetromino.centerY

        if input == "right":
            tetromino.update_pos(prevCenterX + Block.dim, prevCenterY)
            
        elif input == "left":
            tetromino.update_pos(prevCenterX - Block.dim, prevCenterY)

        if (self.checkOutOrCollide(tetromino) or self.checkBelow(tetromino)):
                tetromino.update_pos(prevCenterX, prevCenterY)
    
    def tryRotate(self, tetromino, input):
        if input == "clockwise":
            tetromino.rotate(90)
            if (tetromino == self.falling):
                self.shadow.rotate(90)
            if (self.checkOutOrCollide(tetromino) or self.checkBelow(tetromino)):
                tetromino.rotate(-90)
                if (tetromino == self.falling):
                    self.shadow.rotate(-90)
                return 0
        elif input == "counter":
            tetromino.rotate(-90)
            if (tetromino == self.falling):
                self.shadow.rotate(-90)
            if (self.checkOutOrCollide(tetromino) or self.checkBelow(tetromino)):
                # if (self.checkOutOrCollide(tetromino)):
                #     print("out of bounds")
                # if (self.checkBelow(tetromino)):
                #     print("something underneath")
                
                tetromino.rotate(90)
                if (tetromino == self.falling):
                    self.shadow.rotate(90)
                return 0
        elif input == "flip":
            tetromino.rotate(180)
            if (tetromino == self.falling):
                self.shadow.rotate(180)
            if (self.checkOutOrCollide(tetromino) or self.checkBelow(tetromino)):
                tetromino.rotate(180)
                if (tetromino == self.falling):
                    self.shadow.rotate(180)
                return 0
            
        return 1
        
    def tick(self):
        self.falling.fall()
        if (self.checkBelow(self.falling)):
            self.ticksTouching += 1
            self.falling.update_pos(self.falling.centerX, self.falling.centerY - Block.dim)
            if self.ticksTouching == 50:
                self.place()
        else:
            self.ticksTouching = 0


# shadows

    def spawnShadow(self):

        match self.falling.name:
            case "I_Piece":
                return I_Shadow(0,0)
            case "J_Piece":
                return J_Shadow(0,0)
            case "L_Piece":
                return L_Shadow(0,0)
            case "O_Piece":
                return O_Shadow(0,0)
            case "S_Piece":
                return S_Shadow(0,0)
            case "Z_Piece":
                return Z_Shadow(0,0)
            case "T_Piece":
                return T_Shadow(0,0)
            
    def dropShadow(self):
        while (not self.checkBelowShadow()):
            self.shadow.fall()

        self.shadow.update_pos(self.shadow.centerX, self.shadow.centerY - Block.dim)    
    
    def checkBelowShadow(self):
        blocks = self.shadow.return_blocks()
        for block in blocks:

            if block.y >= 24 * Block.dim or self.onGroundBool[int(block.x / Block.dim) - 7][int(block.y / Block.dim)]:
                return True

        return False
    
    def countShadowHoles(self):
        tetroBlocks = self.shadow.return_blocks()
        holes = 0

        y = 1

        for block in tetroBlocks:
            holeUnder = True
            y = 1
            while holeUnder:
                for block2 in tetroBlocks:
                    if block.colliding(block2): 
                        continue
                    if block2.x == block.x and block2.y == block.y + y * Block.dim:
                        holeUnder = False
                        #print ("under is shadow")
                        break
                
                if int(block.y / Block.dim) + y > 22:
                    #print("under is floor")
                    break
                
                # print(block.x / Block.dim)
                # print(block.y / Block.dim)

                if self.onGroundBool[int(block.x / Block.dim) - 7][int(block.y / Block.dim) + y]:
                    #print ("under is block")
                    break

                if holeUnder:
                    holes += 1
                y+= 1

        return holes
            
        

# checks

    def checkBelow(self, tetromino):
        blocks = tetromino.return_blocks()
        for block in blocks:

            if block.y >= 24 * Block.dim or self.onGroundBool[int(block.x / Block.dim) - 7][int(block.y / Block.dim)]:
                return True
            
        return False

    def checkOutOrCollide(self, tetromino):
        blocks = tetromino.return_blocks()
        for block in blocks:

            #check outofbounds and collide
            if block.x < 7 * Block.dim or block.x >= 17 * Block.dim or block.y >= 23 * Block.dim or self.onGroundBool[int(block.x / Block.dim) - 7][int(block.y / Block.dim)]:
                return True

        return False
    
    def checkLine(self, height):
        for i in range (10):
            if (not self.onGroundBool[i][height]):
                return
        
        self.clearLine(height)
        return True # can use to find the amount of line that are cleared, to work the score

    def clearLine(self, height):
              
        for i in range(int(height)): #starts at 0 and goes to height - 1
            for j in range(10):
                self.onGroundBool[j][height - i] = self.onGroundBool[j][height - i - 1]
                self.onGroundBlock[j][height - i] = self.onGroundBlock[j][height - i - 1]

# AI Moves
                
 # there are 5 first level choices (differs for i piece and o piece as they are symmetrical)
    #   dont rotate
    #   rotate 90
    #   rotate -90
    #   rotate 180
    #   hold

    # within the first 3 choices you can also (10, 9, 8, or 7 choices depending on orientation)
    #   move to left
    #   move to left and move once to right
    #   repeat
                
    def AI_move(self):
        #look at the current piece, make an imaginary piece, and then simulate it through all the possible moves, and if it is not holdable then don't consider that move
        # if it is an O piece then find the 
        # treat more as brute force, while creating a 3 variable list and then appending it to a 2d list, the first 2 ints are the moves and the last is the quality of the move
        noHold = []

        match self.falling.name: #all the possible cases for the first block
            case "I_Piece": 
                noHold.extend(self.calcMoves("I"))
            case "O_Piece": 
                noHold.extend(self.calcMoves("O"))
            case "S_Piece":
                noHold.extend(self.calcMoves("S"))
            case "Z_Piece":
                noHold.extend(self.calcMoves("Z"))
            case _:
                noHold.extend(self.calcMoves(self.falling.name[0:1])) 

        noHold.sort()

        name = self.falling.name

        if (self.holdable):
            hold = []
            
            

            if (self.holdPiece == None):


                lookingAt = self.q.get()

                self.q.put(lookingAt)

                for i in range(4):
                    self.q.put(self.q.get())
            else:
                lookingAt = self.holdPiece
            
            #print(firstInQueue.name)

            match lookingAt.name: #all the possible cases for the first block
                case "I_Piece": 
                    hold.extend(self.calcMoves("I"))
                case "O_Piece": 
                    hold.extend(self.calcMoves("O"))
                case "S_Piece":
                    hold.extend(self.calcMoves("S"))
                case "Z_Piece":
                    hold.extend(self.calcMoves("Z"))
                case _:
                    hold.extend(self.calcMoves(lookingAt.name[0:1]))

            hold.sort()

            if (noHold[0][0] <= hold[0][0]):
                self.make_move(noHold[0][1], noHold[0][2])
                return name + "  " + str([0, noHold[0]])
            else:
                self.hold()
                self.make_move(hold[0][1], hold[0][2])
                return lookingAt.name + "  " + str([1, hold[0]])

        else:
            self.make_move(noHold[0][1], noHold[0][2])
            return name + "  " + str([0, noHold[0]])

    

    def calcMoves(self, tetromino): #calculate all possible rotations and their holes for the piece

        moves = []

        if (tetromino == "I" or tetromino == "S" or tetromino == "Z"):

            
            if tetromino == "I":
                fakePiece = I_Block(Block.dim * 12, Block.dim * 2)
            elif tetromino == "S":
                fakePiece = S_Block(Block.dim * 11, Block.dim * 2)
            else:
                fakePiece = Z_Block(Block.dim * 11, Block.dim * 2)
            
            moves.extend(self.helper(fakePiece, 0))

            if tetromino == "I":
                fakePiece = I_Block(Block.dim * 12, Block.dim * 2)
            elif tetromino == "S":
                fakePiece = S_Block(Block.dim * 11, Block.dim * 2)
            else:
                fakePiece = Z_Block(Block.dim * 11, Block.dim * 2)

            didntWork = False

            if (self.tryRotate(fakePiece, "counter") == 0):
                print("fuck")
                didntWork = True
                fakePiece.rotate(-90)

                for block in fakePiece.return_blocks():
                    print(str(block.x) + " " + str(block.y))

                fakePiece.rotate(90)
                
                    

            moves.extend(self.helper(fakePiece, 1))

            if didntWork:
                print(tetromino + "   " + str(moves))
           
            
        elif (tetromino == "O"):
            fakePiece = O_Block(Block.dim * 12, Block.dim)
            moves.extend(self.helper(fakePiece, 0))


        else:
            if tetromino == "T":
                fakePiece = T_Block(Block.dim * 11, Block.dim * 2)
            elif tetromino == "L":
                fakePiece = L_Block(Block.dim * 11, Block.dim * 2)
            else:
                fakePiece = J_Block(Block.dim * 11, Block.dim * 2)

            moves.extend(self.helper(fakePiece, 0))

            if tetromino == "T":
                fakePiece = T_Block(Block.dim * 11, Block.dim * 2)
            elif tetromino == "L":
                fakePiece = L_Block(Block.dim * 11, Block.dim * 2)
            else:
                fakePiece = J_Block(Block.dim * 11, Block.dim * 2)

            self.tryRotate(fakePiece, "counter")
            moves.extend(self.helper(fakePiece, 1))

            if tetromino == "T":
                fakePiece = T_Block(Block.dim * 11, Block.dim * 2)
            elif tetromino == "L":
                fakePiece = L_Block(Block.dim * 11, Block.dim * 2)
            else:
                fakePiece = J_Block(Block.dim * 11, Block.dim * 2)

            self.tryRotate(fakePiece, "flip")
            moves.extend(self.helper(fakePiece, 2))

            if tetromino == "T":
                fakePiece = T_Block(Block.dim * 11, Block.dim * 2)
            elif tetromino == "L":
                fakePiece = L_Block(Block.dim * 11, Block.dim * 2)
            else:
                fakePiece = J_Block(Block.dim * 11, Block.dim * 2)

            self.tryRotate(fakePiece, "clockwise")
            moves.extend(self.helper(fakePiece, 3))

        

        return moves
    

    def helper(self, tetromino, rotation):

        moves = []

        for i in range (6):
            self.tryMove(tetromino, "left")

        moves.append([self.evalMove(tetromino, rotation), rotation, 0])

        blocks = tetromino.return_blocks()
        heights = set()

        for block in blocks:
            heights.add(block.x)

        for i in range(10 - len(heights) + 1):
            self.tryMove(tetromino, "right")
            moves.append([self.evalMove(tetromino, rotation), rotation, i + 1])
        
        return moves
    
    def evalMove(self, tetromino, rotation):

        # factors to consider:
        #  - lines cleared, make it scale exponentially, 4 lines is a lot better than 1
        #  - holes made
        #  - flatness of new board
        #  - in the right most and not a line block
        #  - height of the placed block
        #  - death with placement

        startingUnevenness = 0

        first = 0
        second = 0

        for y in range(23):
            if (self.onGroundBool[0][23 - y]):
                first = 23 - y

        for x in range(9): #find the highest block in each column

            for y in range (23):

                if (self.onGroundBool[x][23 - y]):
                    second = y

            startingUnevenness += abs(first - second)

            first = second
            second = 0

        match tetromino.name:
            case "I_Piece":
                fakeShadow = I_Block(Block.dim * 12, Block.dim * 2)
            case "J_Piece":
                fakeShadow = J_Block(Block.dim * 11, Block.dim * 2)
            case "L_Piece":
                fakeShadow = L_Block(Block.dim * 11, Block.dim * 2)
            case "O_Piece":
                fakeShadow = O_Block(Block.dim * 12, Block.dim * 2)
            case "S_Piece":
                fakeShadow = S_Block(Block.dim * 11, Block.dim * 2)
            case "Z_Piece":
                fakeShadow = Z_Block(Block.dim * 11, Block.dim * 2)
            case "T_Piece":
                fakeShadow = T_Block(Block.dim * 11, Block.dim * 2)

        match rotation:
            case 0:
                pass
            case 1:
                self.tryRotate(fakeShadow, "counter")
            case 2:
                self.tryRotate(fakeShadow, "flip")
            case 3:
                self.tryRotate(fakeShadow, "clockwise")

        fakeShadow.update_pos(tetromino.centerX, tetromino.centerY)

        while (not self.checkBelow(fakeShadow)):
            fakeShadow.fall()
        
        fakeShadow.update_pos(fakeShadow.centerX, fakeShadow.centerY - Block.dim)

        tetroBlocks = fakeShadow.return_blocks()

        heights = set()

        for block in tetroBlocks: #check if any lines are cleared using the ys
            heights.add(block.y)

        linesCleared = 0

        loss = False

        for yValue in heights: #check if all the positions are taken in the row
            hasEmpty = False

            if (yValue > 3):
                loss = True


            for xValue in range(10): #xValue = xValue * Block.dim + 
                colliding = False
                for block in tetroBlocks: #check if it is colliding with any of the shadow blocks
                    if block.x == xValue * Block.dim + Block.dim * 7 and block.y == yValue:
                        colliding = True
                        break
                if (not self.onGroundBool[xValue][int(yValue/Block.dim)] and not colliding): #if it isnt colliding with the shadow block and not colliding with the 
                    hasEmpty = True
                    break

            if not hasEmpty:
                linesCleared += 1
        
        uneveness = 0
        overRight = False

        first = 0
        second = 0

        for y in range(23):
            if (self.onGroundBool[0][23 - y]):
                first = 23 - y

            for block in tetroBlocks:
                if block.x == Block.dim + Block.dim * 7 and block.y == (23 - y) * Block.dim:
                    first = 23 - y

        for x in range(9): #find the highest block in each column

            for y in range (23):

                if (self.onGroundBool[x][23 - y]):
                    second = y
                for block in tetroBlocks:
                    if block.x == x * Block.dim + Block.dim * 7 and block.y == (23 - y) * Block.dim:
                        second = 23 - y

            uneveness += abs(first - second)

            first = second
            second = 0
        
        
                    

        holes = 0

        y = 1
        lowY = 100
        highY = -1



        for block in tetroBlocks:
            holeUnder = True
            y = 1

            lowY = min(lowY, 24 - block.y / Block.dim)
            highY = max(highY, 24 - block.y / Block.dim)
            while holeUnder:
                for block2 in tetroBlocks:
                    if block.colliding(block2): 
                        continue
                    if block2.x == block.x and block2.y == block.y + y * Block.dim:
                        holeUnder = False
                        #print ("under is shadow")
                        break
                
                if int(block.y / Block.dim) + y > 23:
                    #print("under is floor")
                    break
                
                # print(block.x / Block.dim)
                # print(block.y / Block.dim)

                if self.onGroundBool[int(block.x / Block.dim) - 7][int(block.y / Block.dim) + y]:
                    #print ("under is block")
                    break

                if holeUnder:
                    holes += 1
                y+= 1

        
        for block in tetroBlocks: # checking for if the block is covering on the right column
            if (block.x == Block.dim * 16): 
                overRight = True

        secondLast = 0
        veryLast = 0

        for y in range (23):

            if (self.onGroundBool[8][23 - y]):
                secondLast = y
            for block in tetroBlocks:
                if block.x == (x + 8) * Block.dim + Block.dim * 7 and block.y == (23 - y) * Block.dim:
                    secondLast = 23 - y

        for y in range (23):

            if (self.onGroundBool[9][23 - y]):
                veryLast = y
            for block in tetroBlocks:
                if block.x == (x + 8) * Block.dim + Block.dim * 7 and block.y == (23 - y) * Block.dim:
                    veryLast = 23 - y


        lastHeight = abs(veryLast - secondLast)


        rating = (holes / ((lowY + highY) / 2) * 3)+ ((lowY + highY )/ 4) + uneveness/30 - (linesCleared * linesCleared)

        #first count if holes are under then do this
        # if (overRight and tetromino.name != 'I_Piece'):
        #     rating += 5
        # elif (overRight and tetromino.name == 'I_Piece' and lastHeight < 4):
        #     rating += 3
        # elif (overRight and tetromino.name == 'I_Piece'):
        #     rating -= 5


        # if (linesCleared == 1):
        #     rating -= 1
        # elif (linesCleared == 2):
        #     rating -= 4
        # elif (linesCleared == 3):
        #     rating -= 9
        # elif (linesCleared == 4):
        #     rating -= 20

        # return [linesCleared, holes, (lowY + highY)/2, abs(startingUnevenness - uneveness), loss, right]
        

        
        
        

        if (loss):
            rating += 20
        

        

        return rating
    
    

    def make_move(self, rotate, movements):
        match rotate:
            case 0:
                pass
            case 1:
                self.tryRotate(self.falling, "counter")
            case 2:
                self.tryRotate(self.falling, "flip")
            case 3: 
                self.tryRotate(self.falling, "clockwise")
            

        for i in range (6):
            self.tryMove(self.falling, "left")

        for i in range(movements):
            self.tryMove(self.falling, "right")

        self.hardDrop()
        
    def possibleMoves(self):
        noHold = []

        match self.falling.name: #all the possible cases for the first block
            case "I_Piece": 
                noHold.extend(self.findMoves("I", 0))
            case "O_Piece": 
                noHold.extend(self.findMoves("O", 0))
            case "S_Piece":
                noHold.extend(self.findMoves("S", 0))
            case "Z_Piece":
                noHold.extend(self.findMoves("Z", 0))
            case _:
                noHold.extend(self.findMoves(self.falling.name[0:1], 0)) 

        name = self.falling.name

        if (self.holdable and self.holdPiece != None):
            hold = []
            
            

            if (self.holdPiece == None):


                lookingAt = self.q.get()

                self.q.put(lookingAt)

                for i in range(4):
                    self.q.put(self.q.get())
            else:
                lookingAt = self.holdPiece
            
            #print(firstInQueue.name)

            match lookingAt.name: #all the possible cases for the first block
                case "I_Piece": 
                    hold.extend(self.findMoves("I", 1))
                case "O_Piece": 
                    hold.extend(self.findMoves("O", 1))
                case "S_Piece":
                    hold.extend(self.findMoves("S", 1))
                case "Z_Piece":
                    hold.extend(self.findMoves("Z", 1))
                case _:
                    hold.extend(self.findMoves(lookingAt.name[0:1]), 1)

            return noHold + hold
        
        return noHold
            
        
        
        
        pass

    def findMoves(self, tetromino, holding):
        moves = []

        if (tetromino == "I" or tetromino == "S" or tetromino == "Z"):

            
            if tetromino == "I":
                fakePiece = I_Block(Block.dim * 12, Block.dim * 2)
            elif tetromino == "S":
                fakePiece = S_Block(Block.dim * 11, Block.dim * 2)
            else:
                fakePiece = Z_Block(Block.dim * 11, Block.dim * 2)
            
            moves.extend(self.helperNew(fakePiece, 0, holding))

            if tetromino == "I":
                fakePiece = I_Block(Block.dim * 12, Block.dim * 2)
            elif tetromino == "S":
                fakePiece = S_Block(Block.dim * 11, Block.dim * 2)
            else:
                fakePiece = Z_Block(Block.dim * 11, Block.dim * 2)

            # didntWork = False

            # if (self.tryRotate(fakePiece, "counter") == 0):
            #     print("fuck")
            #     didntWork = True
            #     fakePiece.rotate(-90)

            #     for block in fakePiece.return_blocks():
            #         print(str(block.x) + " " + str(block.y))

            #     fakePiece.rotate(90)
                
                    

            moves.extend(self.helperNew(fakePiece, 1, holding))

            # if didntWork:
            #     print(tetromino + "   " + str(moves))
           
            
        elif (tetromino == "O"):
            fakePiece = O_Block(Block.dim * 12, Block.dim)
            moves.extend(self.helperNew(fakePiece, 0, holding))


        else:
            if tetromino == "T":
                fakePiece = T_Block(Block.dim * 11, Block.dim * 2)
            elif tetromino == "L":
                fakePiece = L_Block(Block.dim * 11, Block.dim * 2)
            else:
                fakePiece = J_Block(Block.dim * 11, Block.dim * 2)

            moves.extend(self.helperNew(fakePiece, 0, holding))

            if tetromino == "T":
                fakePiece = T_Block(Block.dim * 11, Block.dim * 2)
            elif tetromino == "L":
                fakePiece = L_Block(Block.dim * 11, Block.dim * 2)
            else:
                fakePiece = J_Block(Block.dim * 11, Block.dim * 2)

            self.tryRotate(fakePiece, "counter")
            moves.extend(self.helperNew(fakePiece, 1, holding))

            if tetromino == "T":
                fakePiece = T_Block(Block.dim * 11, Block.dim * 2)
            elif tetromino == "L":
                fakePiece = L_Block(Block.dim * 11, Block.dim * 2)
            else:
                fakePiece = J_Block(Block.dim * 11, Block.dim * 2)

            self.tryRotate(fakePiece, "flip")
            moves.extend(self.helperNew(fakePiece, 2, holding))

            if tetromino == "T":
                fakePiece = T_Block(Block.dim * 11, Block.dim * 2)
            elif tetromino == "L":
                fakePiece = L_Block(Block.dim * 11, Block.dim * 2)
            else:
                fakePiece = J_Block(Block.dim * 11, Block.dim * 2)

            self.tryRotate(fakePiece, "clockwise")
            moves.extend(self.helperNew(fakePiece, 3, holding))

        

        return moves
    
    def helperNew(self, tetromino, rotation, holding):

        moves = []

        for i in range (6):
            self.tryMove(tetromino, "left")

        moves.append([holding, rotation, 0])

        blocks = tetromino.return_blocks()
        heights = set()

        for block in blocks:
            heights.add(block.x)

        for i in range(10 - len(heights) + 1):
            self.tryMove(tetromino, "right")
            moves.append([holding, rotation, i + 1])

        return moves


    def evalMoveNew(self, tetromino, displacement, rotation):

        # factors to consider:
        #  - lines cleared, make it scale exponentially, 4 lines is a lot better than 1
        #  - holes made
        #  - flatness of new board
        #  - in the right most and not a line block
        #  - height of the placed block
        #  - death with placement

        first = 0
        second = 0

        startingUnevenness = 0

        for y in range(23):
            if (self.onGroundBool[0][23 - y]):
                first = 23 - y

        for x in range(9): #find the highest block in each column

            for y in range (23):

                if (self.onGroundBool[x][23 - y]):
                    second = y

            startingUnevenness += abs(first - second)

            first = second
            second = 0

        match tetromino:
            case "I_Piece":
                fakeShadow = I_Block(Block.dim * 12, Block.dim * 2)
            case "J_Piece":
                fakeShadow = J_Block(Block.dim * 11, Block.dim * 2)
            case "L_Piece":
                fakeShadow = L_Block(Block.dim * 11, Block.dim * 2)
            case "O_Piece":
                fakeShadow = O_Block(Block.dim * 12, Block.dim * 2)
            case "S_Piece":
                fakeShadow = S_Block(Block.dim * 11, Block.dim * 2)
            case "Z_Piece":
                fakeShadow = Z_Block(Block.dim * 11, Block.dim * 2)
            case "T_Piece":
                fakeShadow = T_Block(Block.dim * 11, Block.dim * 2)

        match rotation:
            case 0:
                pass
            case 1:
                self.tryRotate(fakeShadow, "counter")
            case 2:
                self.tryRotate(fakeShadow, "flip")
            case 3:
                self.tryRotate(fakeShadow, "clockwise")

        

        for i in range (6):
            self.tryMove(fakeShadow, "left")

        for i in range(displacement):
            self.tryMove(fakeShadow, "right")

        while (not self.checkBelow(fakeShadow)):
            fakeShadow.fall()
        
        fakeShadow.update_pos(fakeShadow.centerX, fakeShadow.centerY - Block.dim)

        tetroBlocks = fakeShadow.return_blocks()

        heights = set()

        for block in tetroBlocks: #check if any lines are cleared using the ys
            heights.add(block.y)

        linesCleared = 0

        loss = False

        for yValue in heights: #check if all the positions are taken in the row
            hasEmpty = False

            if (yValue > 3):
                loss = True


            for xValue in range(10): #xValue = xValue * Block.dim + 
                colliding = False
                for block in tetroBlocks: #check if it is colliding with any of the shadow blocks
                    if block.x == xValue * Block.dim + Block.dim * 7 and block.y == yValue:
                        colliding = True
                        break
                if (not self.onGroundBool[xValue][int(yValue/Block.dim)] and not colliding): #if it isnt colliding with the shadow block and not colliding with the 
                    hasEmpty = True
                    break

            if not hasEmpty:
                linesCleared += 1
        
        uneveness = 0
        overRight = False

        first = 0
        second = 0

        for y in range(23):
            if (self.onGroundBool[0][23 - y]):
                first = 23 - y

            for block in tetroBlocks:
                if block.x == Block.dim + Block.dim * 7 and block.y == (23 - y) * Block.dim:
                    first = 23 - y

        for x in range(9): #find the highest block in each column

            for y in range (23):

                if (self.onGroundBool[x][23 - y]):
                    second = y
                for block in tetroBlocks:
                    if block.x == x * Block.dim + Block.dim * 7 and block.y == (23 - y) * Block.dim:
                        second = 23 - y

            uneveness += abs(first - second)

            first = second
            second = 0
        
        
                    

        holes = 0

        y = 1
        lowY = 100
        highY = -1



        for block in tetroBlocks:
            holeUnder = True
            y = 1

            lowY = min(lowY, 24 - block.y / Block.dim)
            highY = max(highY, 24 - block.y / Block.dim)
            while holeUnder:
                for block2 in tetroBlocks:
                    if block.colliding(block2): 
                        continue
                    if block2.x == block.x and block2.y == block.y + y * Block.dim:
                        holeUnder = False
                        #print ("under is shadow")
                        break
                
                if int(block.y / Block.dim) + y > 23:
                    #print("under is floor")
                    break
                
                # print(block.x / Block.dim)
                # print(block.y / Block.dim)

                if self.onGroundBool[int(block.x / Block.dim) - 7][int(block.y / Block.dim) + y]:
                    #print ("under is block")
                    break

                if holeUnder:
                    holes += 1
                y+= 1

        
        for block in tetroBlocks: # checking for if the block is covering on the right column
            if (block.x == Block.dim * 16): 
                overRight = True

        secondLast = 0
        veryLast = 0

        for y in range (23):

            if (self.onGroundBool[8][23 - y]):
                secondLast = y
            for block in tetroBlocks:
                if block.x == (x + 8) * Block.dim + Block.dim * 7 and block.y == (23 - y) * Block.dim:
                    secondLast = 23 - y

        for y in range (23):

            if (self.onGroundBool[9][23 - y]):
                veryLast = y
            for block in tetroBlocks:
                if block.x == (x + 8) * Block.dim + Block.dim * 7 and block.y == (23 - y) * Block.dim:
                    veryLast = 23 - y


        lastHeight = abs(veryLast - secondLast)

        right = 0

        if (overRight and tetromino.name != 'I_Piece'):
            right = -2
        elif (overRight and tetromino.name == 'I_Piece' and lastHeight < 4):
            right = -1
        elif (overRight and tetromino.name == 'I_Piece'):
            right = 1

        status = [linesCleared, -holes, -(lowY + highY)/2, -abs(startingUnevenness - uneveness), -loss, right]
        
        for i in range(10):
            for j in range (24):
                if self.onGroundBool[i][j]:
                    status.append(1)
                else:
                    status.append(0)

        return status
        
        
        # rating = (holes /((lowY + highY) /2) * 3)+ ((lowY + highY )/ 4) - (linesCleared * linesCleared) + uneveness/30

        # if (loss):
        #     rating += 20

        

        # return rating
    
        
        


    def make_move_New(self, hold, rotate, movements):

        if (hold == 1):
            self.hold()

        match rotate:
            case 0:
                pass
            case 1:
                self.tryRotate(self.falling, "counter")
            case 2:
                self.tryRotate(self.falling, "flip")
            case 3: 
                self.tryRotate(self.falling, "clockwise")
            

        for i in range (6):
            self.tryMove(self.falling, "left")

        for i in range(movements):
            self.tryMove(self.falling, "right")

        self.hardDrop()


    # def AI_move1(self):


    #     maxMoves = 0

    #     match self.falling.name:
    #         case "I_Piece": 
    #             maxMoves = 3 #hold, rotate, and keep
    #         case "O_Piece": 
    #             maxMoves = 2
    #         case "S_Piece":
    #             maxMoves = 3 #hold and keep
    #         case "Z_Piece":
    #             maxMoves = 3
    #         case _:
    #             maxMoves = 5 #all rotates, hold, and keep

    #     #pick a random number between all these 

    #     moves = []

    #     for i in range(1, maxMoves + 1):
    #         moves.append(i)

    #     if (not self.holdable):
    #         moves.remove(2)

    #     #print(moves)
    #     choice = random.choice(moves) 
    #     #if not self.holdable:


    #     match choice:
    #         case 1:
    #             pass
    #         case 2:
    #             self.hold()
    #             return
    #         case 3:
    #             self.tryRotate("clockwise")
    #         case 4:
    #             self.tryRotate("counter")
    #         case 5: 
    #             self.tryRotate("flip")
       
        

    #     self.AI_move2()

    # def AI_move2(self):

    #     #first count the max amount of blocks that are in a row, to decide the amount of choices that can occur

    #     blocks = self.falling.return_blocks()
    #     heights = set()
    #     sameX = 0

    #     for block in blocks:
    #         heights.add(block.x)
        


    #     sameX = len(heights)

    #     #4 = 7, 3 = 8, 2 = 9, 1 = 10
        

    #     choices = 10 - sameX + 1
    #     #print(choices - 1)

    #     for i in range (6):
    #         self.tryMove(self.falling, "left")

    #     choice = random.randint(0, choices - 1)

    #     #print(choice)

    #     for i in range(choice):
    #         self.tryMove(self.falling, "right")

    #     self.hardDrop()


# misc

    def spawnRandom(self):
        ##r.seed()
        rand = m.trunc(r.randint(0,6))

        match rand:
            case 0:
                return I_Block(0, 0)
            case 1:
                return J_Block(0, 0)
            case 2:
                return L_Block(0, 0)
            case 3:
                return O_Block(0, 0)
            case 4:
                return S_Block(0, 0)
            case 5:
                return Z_Block(0, 0)
            case _:
                return T_Block(0, 0)
            
    def spawnfrom7bag(self):
        self.q.put(self.bag[self.bagIndex])

        self.bagIndex += 1

        if self.bagIndex == 7:
            self.bag = [I_Block(0, 0), J_Block(0, 0), L_Block(0, 0), O_Block(0, 0), S_Block(0, 0), Z_Block(0, 0), T_Block(0, 0)]
            random.shuffle(self.bag)
            self.bagIndex = 0
