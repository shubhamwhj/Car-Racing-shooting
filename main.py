import pygame, sys, random

from game import gameplay, create_screen
#initializing pygame
pygame.init()
clock=pygame.time.Clock()

#Screen setup
screen=create_screen()

#Loading image surfaces
bg_surf=pygame.image.load("assets/game_road.png") 

#variables rlated to the game
bg_y=-1200 #variable to control bg movement

game_state="initial"

#game loop
while True:
    screen.blit(bg_surf,[0,bg_y])
                
    game_state=gameplay() 
    
    if game_state=="play":
        
        #move background
        if bg_y>-800:
            bg_y=-1200
        bg_y+=10
        

    pygame.display.flip()    
    clock.tick(30)