import pygame, sys, random
#initializing pygame
pygame.init()
clock=pygame.time.Clock()

#Screen setup
screen_width=600
screen_height=600
screen=pygame.display.set_mode((screen_width,screen_height))


def create_screen():
    global screen
    return screen

#font
score_font=pygame.font.Font('freesansbold.ttf', 16)


#funtion to load and scale the given set of images
def load_animations(path_list,scale=1):
    animation_surf_list=[]
    for img_path in path_list:
        surf=pygame.image.load(img_path).convert_alpha()
        if scale!=1:
            surf = pygame.transform.scale(surf,(int(surf.get_width()*scale),int(surf.get_height()*scale)))
        animation_surf_list.append(surf)
    return animation_surf_list;

#function to flip the images
def flip_animations(surf_list):
    flip_surf_list=[]
    for surf in surf_list:
        surf=pygame.transform.flip(surf,True,False)
        flip_surf_list.append(surf)
    return flip_surf_list

#Loading image surfaces
bg_surf=pygame.image.load("assets/game_road.png") 
car1_surf=pygame.image.load("assets/car1.png")
bullet_surf=pygame.image.load("assets/bullet.png")
small_blast_surf=pygame.image.load("assets/smallblast.png")
muzzel_blast_surf=pygame.image.load("assets/blast1.png")
big_blast_surf=pygame.image.load("assets/bigblast.png")
start_msg_surf=pygame.image.load("assets/startmsg.png")
over_msg_surf=pygame.image.load("assets/overmsg.jpg")
cars_surf_list=load_animations(["assets/car2.png","assets/car3.png","assets/car4.png","assets/car5.png"])
power_surf_list=load_animations(["assets/shield.png","assets/bulletp.png","assets/money.jpg","assets/wrench.png"])

#creating list for enemy cars/ bullets/ powerups
enemy_cars=[]
bullets=[]
power_ups=[]

#function to create a new enemy
def spawn_enemy():    
    x_pos=random.randint(100, 450)
    enemy_car=pygame.Rect(x_pos,-150,50,110)
    type=random.randint(0, 3)
    enemy_health=100
    enemy_cars.append([enemy_car,type,enemy_health])

#function to create and shoot a bullet
def shoot_bullet(x_pos,y_pos):
    bullet=pygame.Rect(x_pos,y_pos,10,10)
    bullets.append(bullet)

#function to spawn a powerup
def spawn_power_up(x_pos,y_pos):
    power=pygame.Rect(x_pos,y_pos,50,50)
    power_type=random.randint(0, 3)
    power_duration=100
    power_ups.append([power,power_type,power_duration])
    
#creating player car    
player_car=pygame.Rect(200,480,50,100)



#variables rlated to the game
dx=0 #move player by dx
bg_y=-1200 #variable to control bg movement
gamestate="initial"
cars_counter=0
bullet_counter=0
player_health=100
player_power="NA"
player_money=0
num_of_bullets=1
score=0
power_collected=False

#game loop
def gameplay():
    global gamestate, score, screen
    global bg_y, cars_counter, bullet_counter, power_collected, dx, num_of_bullets
    global player_health, player_power
    global bg_surf
    
    
    screen.blit(bg_surf,[00,bg_y])
   
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                dx=5
            if event.key==pygame.K_LEFT:
                dx=-5
            if event.key==pygame.K_SPACE and gamestate=="initial":
                gamestate="play"
            if event.key==pygame.K_r and gamestate=="end":
                gamestate="play"
                score=0
                player_power="NA"
                player_health=100
                bullet_counter=0            
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT:
                dx=0
            if event.key==pygame.K_LEFT:
                dx=0
                
    if gamestate=="initial":
        screen.blit(start_msg_surf,[135,300])
        
    if gamestate=="play":
        
        score+=1
        
        #move background
        #if bg_y>-800:
         #   bg_y=-1200
        #bg_y+=10
        bg_y=30000
        #move player
        if player_car.x<470 and dx>0: 
            player_car.x+=dx
        if player_car.x>90 and dx<0:
            player_car.x+=dx
            
        #counters to control creation of enemies and shooting of bullets
        cars_counter+=1
        bullet_counter+=1
        
        if cars_counter%50==0:
            spawn_enemy()
        if bullet_counter%10==0:
            shoot_bullet(player_car.x+20 , player_car.y)
            screen.blit(muzzel_blast_surf,(player_car.x+15,player_car.y-20))
        
        #Setting the number of bullets to 2 if player gets the shooting powerup
        if player_power =="double_bullets":
            num_of_bullets=2
         
        #moving all the enemies    
        for enemy in enemy_cars:
            screen.blit(cars_surf_list[enemy[1]], enemy[0])
            pygame.draw.rect(screen,(255,255,255),(enemy[0].x-2,enemy[0].y-16,55,7),0,5)
            pygame.draw.rect(screen,(255,100,0),(enemy[0].x,enemy[0].y-15,int(enemy[2]/2),5),0,5)
            enemy[0].y+=5
            
            #checking collision of enemies with the player car
            if enemy[0].colliderect(player_car):
                if player_power!="shield":
                    player_health-=20
                enemy_cars.remove(enemy)
                screen.blit(big_blast_surf,enemy[0])
                
            #cheching collision of enemies with the bullets    
            for bullet in bullets:
                if bullet.colliderect(enemy[0]):
                    score+=10
                    enemy[2]-=20*num_of_bullets
                    screen.blit(small_blast_surf,(bullet.x-10,bullet.y-20))
                    bullets.remove(bullet)
                    if enemy[2]<20:
                        screen.blit(big_blast_surf,enemy[0])
                        enemy_cars.remove(enemy)
                        score+=100
                        chance=random.randint(0, 3)
                        if chance==enemy[1]:
                            spawn_power_up(enemy[0].x, enemy[0].y)
            
            #cheching if enemy has left the screen and destroying it.
            if enemy[0].y>700:
                screen.blit(big_blast_surf,enemy[0])
                enemy_cars.remove(enemy)
    
        #display and move the bullets on the screen
        for bullet in bullets:
            screen.blit(bullet_surf,bullet)
            if player_power=="double_bullets":
                screen.blit(bullet_surf,(bullet.x+10,bullet.y))
            #pygame.draw.rect(screen, (255,0,0), bullet)
            bullet.y-=10
        
        
        # display the power ups and control which powerup to be displayed
        for power in power_ups:
            power[0].y+=10
            screen.blit(power_surf_list[power[1]],power[0])
            
            if power_collected==True:
                power[2]-=1
                if power[2]==0:
                    print("duration over")
                    player_power="NA"
                    power_ups.remove(power)
                    power_collected=False
                    continue
            
            if power[0].colliderect(player_car):
                power_collected=True
                
                if power[1]==0:
                    player_power="shield"
                    power[2]-=1
                if power[1]==1:
                    player_power="double_bullets"
                if power[1]==2:
                    score+=1000
                if power[1]==3:
                    if player_health<100:
                        player_health+=20
                             
                power_ups.remove(power)
        
        #display the power icon in the game on top left
        if player_power=="shield":
            screen.blit(power_surf_list[0],(10,100))
        if player_power=="double_bullets":
            screen.blit(power_surf_list[1],(10,100))
            
        #cheching if the player health is low and endign the game    
        if player_health<20:
            gamestate="end"
        
        #display score
        score_text=score_font.render(str(score), False, (255,255,255))     
        screen.blit(score_text,[10,30])  
        screen.blit(power_surf_list[2],(10,50))
    
    #end state      
    if gamestate=="end":
        screen.blit(over_msg_surf,[155,140])
        
    
    #display player and player health
    screen.blit(car1_surf,player_car)
    pygame.draw.rect(screen,(255,255,255),(10-3,10,55,7),0,5)
    pygame.draw.rect(screen,(0,255,100),(10,10+1,player_health/2,5),0,5)        
    pygame.display.flip()
    
    return gamestate