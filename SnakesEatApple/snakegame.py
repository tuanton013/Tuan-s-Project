import pygame
from time import sleep
from random import randint

pygame.init()
screen = pygame.display.set_mode((601, 601))
pygame.display.set_caption("Snake")
running = True 
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial",25)
score = 0


# snake position tail to head
snakes = [[5, 6]]

# Direction
direction = "right"

# apple position
apple = [randint(1,19),randint(1,19)]

pausing = False

while running:
	clock.tick(60)
	screen.fill(BLACK)

	tail_x = snakes[0][0]
	tail_y = snakes[0][1]

	# Draw grid
	# for i in range(20):
	# 	pygame.draw.line(screen, WHITE, (0,i*30), (600,i*30))
	# 	pygame.draw.line(screen, WHITE, (i*30,0), (i*30,600))

	# Draw snake
	for snake in snakes:
		pygame.draw.rect(screen,GREEN,(snake[0]*30,snake[1]*30,30,30))

	# out of bound
	if (snakes[-1][0] >= 19) or (snakes[-1][1] >= 19) or (snakes[-1][0] <= 0) or (snakes[-1][1] <= 0):
		pausing = True

	# Draw game over:
	if pausing:
		game_over_txt = font.render("Game over, " + str(score), True, WHITE)
		screen.blit(game_over_txt,(130,300))
		press_continue_txt = font.render("Press enter to continue", True, WHITE)
		screen.blit(press_continue_txt,(130,330))
	
	#snake move
	if pausing == False:
		if direction == "right" and direction != "left":
			snakes.append([snakes[-1][0]+1, snakes[-1][1]])
			snakes.pop(0)
		if direction == "left" and direction != "right":
			snakes.append([snakes[-1][0]-1, snakes[-1][1]])
			snakes.pop(0)
		if direction == "up" and direction != "down":
			snakes.append([snakes[-1][0], snakes[-1][1]-1])
			snakes.pop(0)
		if direction == "down" and direction != "up":
			snakes.append([snakes[-1][0], snakes[-1][1]+1])
			snakes.pop(0)
	
	# crash in body
	for i in range(len(snakes)-1):
		if snakes[-1][0] == snakes[i][0] and snakes[-1][1] == snakes[i][1]:
			pausing = True
	
	sleep(0.05)

	# Draw score
	score_txt = font.render("Score: "+ str(score),True,WHITE)
	screen.blit(score_txt,(0,0))


	# Draw apple
	pygame.draw.rect(screen, RED, (apple[0]*30, apple[1]*30, 30, 30))
	
	# snake eat apple
	if snakes[-1][0] == apple[0] and snakes[-1][1] == apple[1]:
		snakes.insert(0,[tail_x, tail_y])
		score += 1
	
	# special case	
		for snake in snakes:
			if apple != snake:
				apple = [randint(1,19),randint(1,19)]
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				pausing = False
				snakes = [[5, 6]]
				apple = [randint(1,19),randint(1,19)]
				direction = "right"
				score = 0
		if event.type == pygame.KEYDOWN:
			if event.key == ord("w") and direction != "down":
				direction = "up"
			if event.key == ord("s") and direction != "up":
				direction = "down"
			if event.key == ord("a") and direction != "right":
				direction = "left"
			if event.key == ord("d") and direction != "left":
				direction = "right"

	pygame.display.flip()

pygame.quit()