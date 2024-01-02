import pygame

class Block:
    dim = 30
    def __init__ (self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
    def draw (self, screen):
        borderWidth = 1
        pygame.draw.rect(screen, "gray60", pygame.Rect(self.x, self.y, self.dim, self.dim), borderWidth, 0)
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x + borderWidth, self.y + borderWidth, self.dim - (borderWidth * 2), self.dim - (borderWidth * 2)))
    def update_pos (self, x, y):
        self.x = x
        self.y = y
    def colliding (self, other):
        if other.x == self.x and other.y == self.y:
            return True
        
        return False