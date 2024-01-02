import numpy as n
from array import *
from Block import *

class Tetromino:
    def __init__ (self, centerX, centerY):
        self.centerX = centerX
        self.centerY = centerY
        self.name = ""
        self.color = ""
        self.around_blocks = [[0, 0],[0, 0],[0, 0]]
    def draw (self, screen):
        for block in self.return_blocks():
            block.draw(screen)
        
    def rotate (self, degrees):
        multX = 1
        multY = 1

        

        if degrees == -90:
            multX = -1
            multY = -1
         #doesn't work with the corner spots
        if degrees == 180:
            for i in range(3):
                self.around_blocks[i] = [-self.around_blocks[i][0], -self.around_blocks[i][1]]
        else:
            for i in range(3):
                if (self.around_blocks[i] == [1, 1]):
                    self.around_blocks[i] = [-1 * multX, 1 * multY]

                elif (self.around_blocks[i] == [-1, 1]):
                    self.around_blocks[i] = [-1  * multX, -1 * multY]

                elif (self.around_blocks[i] == [-1, -1]):
                    self.around_blocks[i] = [1 * multX, -1 * multY]

                elif (self.around_blocks[i] == [1, -1]):  
                    self.around_blocks[i] = [1 * multX, 1 * multY]

                elif self.around_blocks[i][0] != 0:
                    self.around_blocks[i] = [self.around_blocks[i][1] * multX, self.around_blocks[i][0] * multY]
                else:
                    self.around_blocks[i] = [-self.around_blocks[i][1] * multX, self.around_blocks[i][0] * multY]
    
        
    def update_pos (self, centerX, centerY):
        self.centerX = centerX
        self.centerY = centerY
    def fall (self):
        self.update_pos(self.centerX, self.centerY + Block.dim)

    def return_blocks (self):
        blockList = [Block(self.color, self.centerX, self.centerY)]

        for i in range (3):
            blockList.append(Block(self.color, self.centerX + Block.dim * self.around_blocks[i][0], self.centerY + Block.dim * self.around_blocks[i][1]))
        return blockList




    