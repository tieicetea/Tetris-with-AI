from array import *
from Block import *
from Tetromino import *

class L_Shadow (Tetromino):
    def __init__ (self, centerX, centerY):
        super().__init__(centerX, centerY)
        self.name = "L_Piece"
        self.color = "grey91"
        self.around_blocks = [[-1, 0], [1, 0], [1,-1]]

class J_Shadow (Tetromino):
    def __init__ (self, centerX, centerY):
        super().__init__(centerX, centerY)
        self.name = "J_Piece"
        self.color = "grey91"
        self.around_blocks = [[-1, -1],[-1, 0],[1, 0]]

class T_Shadow(Tetromino):
    # color = "purple"

    # around_blocks = [[0, 1], [1, 0], [0, -1]]


    def __init__ (self, centerX, centerY):
        super().__init__(centerX, centerY)
        self.name = "T_Piece"
        self.color = "grey91"
        self.around_blocks = [[-1, 0],[0, -1], [1, 0]]

class Z_Shadow(Tetromino):
    def __init__(self, centerX, centerY):
        super().__init__(centerX, centerY)
        self.name = "Z_Piece"
        self.color = "grey91"
        self.around_blocks = [[-1, -1], [0, -1], [1, 0]]

class S_Shadow(Tetromino):
    def __init__(self, centerX, centerY):
        super().__init__(centerX, centerY)
        self.name = "S_Piece"
        self.color = "grey91"
        self.around_blocks = [[-1, 0], [0, -1], [1, -1]]

class O_Shadow(Tetromino):
    def __init__(self, centerX, centerY):
        super().__init__(centerX, centerY)
        self.name = "O_Piece"
        self.color = "grey91"
        self.around_blocks  = [[-1, -1], [-1, 0], [0, -1]]
    def rotate(self, degrees):
        self.around_blocks = [[-1, -1], [-1, 0], [0, -1]]

class I_Shadow (Tetromino):
    def __init__(self, centerX, centerY):
        super().__init__(centerX, centerY)
        self.name = "I_Piece"
        self.color = "grey91"
        self.around_blocks  = [[-2, 0],[-1, 0],[1, 0]] 
        #self.center_block  #relation to the ideal center block, do i really need this if im going to use a rotation value
        self.rotation_value  = 3 #0, 1, 2, 3 (0 is vertical block to the right, and increasing by 1 rotates it clockwise)
        # 3 or 4 around blocks???
    def rotate(self, degrees):
        super().rotate(degrees)
        
        if degrees == 90:
            self.rotation_value += 1
        elif degrees == 180:
            self.rotation_value += 2
        else:
            self.rotation_value += 3

        self.rotation_value %= 4
    def draw(self, screen): # draw all 4
        for block in self.return_blocks():
            block.draw(screen)

    def return_blocks (self):
        if self.rotation_value == 0:
            centerBlockX = self.centerX
            centerBlockY = self.centerY
        elif self.rotation_value == 1:
            centerBlockX = self.centerX - Block.dim
            centerBlockY = self.centerY
        elif self.rotation_value == 2:
            centerBlockX = self.centerX - Block.dim
            centerBlockY = self.centerY - Block.dim
        elif self.rotation_value == 3:
            centerBlockX = self.centerX
            centerBlockY = self.centerY - Block.dim

        blockList = [Block(self.color, centerBlockX, centerBlockY)]
        for i in range(3):
            blockList.append(Block(self.color, centerBlockX + Block.dim * self.around_blocks[i][0], centerBlockY + Block.dim * self.around_blocks[i][1]))
        
        return blockList
