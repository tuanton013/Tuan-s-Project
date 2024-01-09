import pygame
import time
import math

pygame.init()

screen = pygame.display.set_mode((500,600))

GREY = (150,150,150)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

running = True

font = pygame.font.SysFont("arial",50)
text_1 = font.render("+",True,BLACK)
text_2 = font.render("+",True,BLACK)
text_3 = font.render("-",True,BLACK)
text_4 = font.render("-",True,BLACK)
text_5 = font.render("Start",True,BLACK)
text_6 = font.render("Reset",True,BLACK)

total_secs = 0 
total = 0
start = False

clock = pygame.time.Clock()

while running:
    clock.tick(60)
    screen.fill(GREY)
    mouse_x,mouse_y = pygame.mouse.get_pos()

    pygame.draw.rect(screen, WHITE,(50,50,60,60))
    screen.blit(text_1,(68,50))
    pygame.draw.rect(screen, WHITE,(200,50,60,60))
    screen.blit(text_2,(220,50))
    pygame.draw.rect(screen, WHITE,(50,200,60,60))
    screen.blit(text_3,(72  ,200))
    pygame.draw.rect(screen, WHITE,(200,200,60,60))
    screen.blit(text_4,(223,200))
    pygame.draw.rect(screen, WHITE,(350,70,110,45))
    screen.blit(text_5,(350,65))
    pygame.draw.rect(screen, WHITE,(350,180,110,45))
    screen.blit(text_6,(350,175))
    pygame.draw.rect(screen, BLACK,(50,500,410,60))
    pygame.draw.rect(screen, WHITE,(65,510,380,40))

    pygame.draw.circle(screen, BLACK,(250,390),80)
    pygame.draw.circle(screen, WHITE,(250,390),75)
    
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 1:
                if ((50 < mouse_x < 110) and (110 > mouse_y > 50)):
                    print("press to + min")
                    total_secs += 60
                    total = total_secs
                if ((50 < mouse_x < 110) and (200 < mouse_y < 260)):
                    print("press to - min")
                    total_secs -= 60
                    total = total_secs
                if ((200 < mouse_x < 260) and (50 < mouse_y < 110)):
                    print("press to + seconds")
                    total_secs += 1
                    total = total_secs
                if ((200 < mouse_x < 260) and (200 < mouse_y < 260)):
                    print("press to - seconds")
                    total_secs -= 1
                    total = total_secs
                if ((350 < mouse_x < 460) and (110 > mouse_y > 50)):
                    start = True
                    total = total_secs
                    print("starting")
                if ((350 < mouse_x < 460) and (180 < mouse_y < 225)):
                    total_secs = 0
                    start = False
                    print("reseting")
                print("total_secs: " + str(total_secs))


    if start:
        total_secs -=1
        if total_secs == 0:
            start = False
        time.sleep(1)

    if total_secs < 0:
        total_secs = 0

                  
    mins = int(total_secs/60)
    seconds = total_secs - mins * 60
    

    time_now = str(mins) + ":" + str(seconds)
    text_time = font.render(time_now,True, BLACK)
    screen.blit(text_time,(100,120))
        
    x_sec = 250+70 * math.sin(6*seconds*math.pi/180)        
    y_sec = 390-70 * math.cos(6*seconds*math.pi/180)    
    pygame.draw.line(screen,BLACK,(250,390),(int(x_sec),int(y_sec)))
    
    x_min = 250+50 * math.sin(6*mins*math.pi/180)        
    y_min = 390-50 * math.cos(6*mins*math.pi/180)    
    pygame.draw.line(screen,RED,(250,390),(int(x_min),int(y_min)))
    pygame.draw.circle(screen, BLACK,(250,390),5)   

    if total != 0:
        pygame.draw.rect(screen, RED,(65,510,int(380 * (total_secs/total)),40))   
    
    pygame.display.flip()

pygame.quit()
