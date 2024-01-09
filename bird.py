import pygame
from random import randint

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
running = True
GREEN = (0, 250, 0)
BLUE = (0, 0, 250)
RED = (230, 0 , 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)

clock = pygame.time.Clock()

TUBE_WIDTH = 50
TUBE_VELOCITY = 3
TUBE_GAP = 150

tube1_x = 500
tube2_x = 700
tube3_x = 900

tube1_height = randint(100, 400)
tube2_height = randint(100, 400)
tube3_height = randint(100, 400)

BIRD_X = 50
bird_y = 300
BIRD_WIDTH = 40
BIRD_HEIGHT = 40
bird_drop_velocity = 0
GRAVITY = 0.5

score = 0
font = pygame.font.SysFont("arial",25)

tube1_pass = False
tube2_pass = False
tube3_pass = False

pausing = False

bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image,(BIRD_WIDTH,BIRD_HEIGHT))

background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image,(WIDTH,HEIGHT))

tube_image = pygame.image.load("tube.png")
tube_image = pygame.transform.scale(tube_image,(TUBE_WIDTH,HEIGHT - TUBE_GAP - tube1_height))

while running:
	clock.tick(60)
	screen.fill(GREEN)
	screen.blit(background_image,(0,0))

	# draw tube
	tube1_rect = pygame.draw.rect(screen, BLUE,(tube1_x, 0, TUBE_WIDTH, tube1_height))
	tube2_rect = pygame.draw.rect(screen, BLUE,(tube2_x, 0, TUBE_WIDTH, tube2_height))
	tube3_rect =pygame.draw.rect(screen, BLUE,(tube3_x, 0, TUBE_WIDTH, tube3_height))

	# tube1_rect = screen.blit(tube_image,(tube1_x, 0))
	# tube2_rect = screen.blit(tube_image,(tube2_x, 0))
	# tube3_rect = screen.blit(tube_image,(tube3_x, 0))
	
	# draw tube inverse
	# tube1_rect_inverse = pygame.draw.rect(screen, BLUE,(tube1_x, TUBE_GAP + tube1_height, TUBE_WIDTH, HEIGHT - TUBE_GAP - tube1_height))
	# tube2_rect_inverse = pygame.draw.rect(screen, BLUE,(tube2_x, TUBE_GAP + tube2_height, TUBE_WIDTH, HEIGHT - TUBE_GAP - tube2_height))
	# tube3_rect_inverse = pygame.draw.rect(screen, BLUE,(tube3_x, TUBE_GAP + tube3_height, TUBE_WIDTH, HEIGHT - TUBE_GAP - tube3_height))

	tube1_rect_inverse = screen.blit(tube_image,(tube1_x,TUBE_GAP + tube1_height))	
	tube2_rect_inverse = screen.blit(tube_image,(tube2_x,TUBE_GAP + tube2_height))
	tube3_rect_inverse = screen.blit(tube_image,(tube3_x,TUBE_GAP + tube3_height))


	# draw bird
	#bird_rect = pygame.draw.rect(screen, RED,(BIRD_X, bird_y, BIRD_WIDTH, BIRD_HEIGHT))
	bird_rect = screen.blit(bird_image,(BIRD_X,bird_y))

	# bird falls
	bird_y += bird_drop_velocity
	bird_drop_velocity += GRAVITY

	tube1_x = tube1_x - TUBE_VELOCITY
	tube2_x = tube2_x - TUBE_VELOCITY
	tube3_x = tube3_x - TUBE_VELOCITY
	

	# generate new tubes
	if tube1_x < -TUBE_WIDTH:
		tube1_x = 550
		tube1_height = randint(100, 400)
		tube1_pass = False
	if tube2_x < -TUBE_WIDTH:
		tube2_x = 550
		tube2_height = randint(100, 400)
		tube2_pass = False
	if tube3_x < -TUBE_WIDTH:
		tube3_x = 550
		tube3_height = randint(100, 400)
		tube3_pass = False

	# score
	font1 = pygame.font.SysFont("arial",50)
	txt_score = font1.render(str(score), True, RED) 
	screen.blit(txt_score,(200,100))
	tube_image = pygame.transform.scale(tube_image,(TUBE_WIDTH,TUBE_GAP + tube1_height))

	# update score
	if tube1_x + TUBE_WIDTH <= BIRD_X and tube1_pass == False:
		score +=1
		tube1_pass = True
	if tube2_x + TUBE_WIDTH <= BIRD_X and tube2_pass == False:
		score +=1
		tube2_pass = True
	if tube3_x + TUBE_WIDTH <= BIRD_X and tube3_pass == False:
		score +=1
		tube3_pass = True

	#check overlap
	for tube in [tube1_rect, tube2_rect, tube3_rect, tube1_rect_inverse, tube2_rect_inverse, tube3_rect_inverse]:
		if bird_rect.colliderect(tube) or bird_y > HEIGHT or bird_y < 0:
			pausing = True
			TUBE_VELOCITY = 0
			bird_drop_velocity = 0
			game_over_txt = font.render("Game over, score: " + str(score), True, BLACK)
			screen.blit(game_over_txt,(130,300))
			press_continue_txt = font.render("Press enter to continue", True, BLACK)
			screen.blit(press_continue_txt,(130,330))


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN: 
				if pausing:
					TUBE_VELOCITY = 3
					bird_y = 300
					tube1_x = 500
					tube2_x = 700
					tube3_x = 900
					pausing = False
					score = 0 	
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				bird_drop_velocity = 0
				bird_drop_velocity -= 8
			
			

	pygame.display.flip()     