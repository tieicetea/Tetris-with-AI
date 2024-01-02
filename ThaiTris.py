from Block import *
from Tetrominoes import *
from Board import *
import numpy as n
# Example file showing a circle moving on screen
import pygame

# pygame setup
def main ():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((720, 810))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    pygame.key.set_repeat(50)
    #block1 = Block("red", player_pos.x, player_pos.y)


    board = Board(screen)
    board.setup()

    tickSpeed =  1

    pygame.time.set_timer(pygame.USEREVENT, tickSpeed)

    startPointsLvl = 0

    clockable = True
    counterable = True
    flippable = True
    hardDropable = True
    resetable = True
    paused = False
    pausable = True

    #run all possible moves, evaluate how good the move is

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                
            
                        
                
                if keys[pygame.K_LEFT]:
                    board.tryMove(board.falling, "left")
                if keys[pygame.K_RIGHT]:
                    board.tryMove(board.falling, "right")

                if keys[pygame.K_p] and pausable:
                    paused = not paused
                    pausable = False

                # make these not work if held
                
                if keys[pygame.K_c] and clockable:
                    board.tryRotate(board.falling, "clockwise")
                    clockable = False
                if keys[pygame.K_z] and counterable:
                    board.tryRotate(board.falling, "counter")
                    counterable = False
                if keys[pygame.K_x] and flippable:
                    board.tryRotate(board.falling, "flip")
                    flippable = False
                if keys[pygame.K_LSHIFT]: #or keys[pygame.K_SPACE]:
                    board.hold()
                if keys[pygame.K_ESCAPE]:
                    running = False
                if keys[pygame.K_DOWN]:
                    board.tick()
                if keys[pygame.K_SPACE] and hardDropable:
                    board.hardDrop()
                    hardDropable = False
                if keys[pygame.K_r] and resetable:
                    board = Board(screen)
                    board.setup()
                    board.lost = False
                    resetable = False
            
        
                
            if event.type == pygame.KEYUP:
                
                keys = pygame.key.get_pressed()
                if not (keys[pygame.K_c] or clockable):
                    clockable = True
                if not (keys[pygame.K_z] or counterable):
                    counterable = True
                if not (keys[pygame.K_x] or flippable):
                    flippable = True
                if not (keys[pygame.K_SPACE] or hardDropable):
                    hardDropable = True
                if not (keys[pygame.K_r] or resetable):
                    resetable = True

                if not (keys[pygame.K_p] or pausable):
                    pausable = True
                
            if event.type == pygame.USEREVENT and not board.lost and not paused:

                board.tick()
                #print(board.countShadowHoles())
                
                print(board.AI_move())
            



        # fill the screen with a color to wipe away anything from last frame
        screen.fill("gray10")
        
        #block1.update_pos(player_pos.x, player_pos.y)
        #block1.draw(screen)
        #usingPiece.update_pos(player_pos.x, player_pos.y)
        #usingPiece.draw(screen)
        board.draw()

        

        
        


        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        #dt = clock.tick(60) / 1000
        clock.tick(120)
    pygame.quit()

    return 5


if __name__ == "__main__":
    main()
    





