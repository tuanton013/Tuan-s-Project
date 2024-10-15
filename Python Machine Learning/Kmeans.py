import pygame
from random import randint
import time
import math
from sklearn.cluster import KMeans

pygame.init()

screen = pygame.display.set_mode((1200, 700))

pygame.display.set_caption("kmeans visualization")

running = True

clock = pygame.time.Clock()

BACKGROUND = (214, 214, 214)
BLACK = (0, 0, 0)
BACKGROUND_PANEL = (249, 255, 230)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
Green = (0, 128, 0)
Blue = (0, 0, 225)
Violet = (238, 130, 238)
Mint = (67, 94, 82)
Yellow = (255, 255, 0)


COLORS = [RED, Green, Blue, Violet, Mint, Yellow]


error = 0
k_count = 0
points = []
clusters = []
labels = []
center = []

font = pygame.font.SysFont('sans', 40)
smaller_font = pygame.font.SysFont('sans', 20)
text_plus = font.render('+', True, WHITE)
text_minus = font.render('-', True, WHITE)
text_run = font.render('Run', True, WHITE)
text_random = font.render('Random', True, WHITE)
text_algorithm = font.render('Algorithm', True, WHITE)
text_reset = font.render('Reset', True, WHITE)


def cluster_random():
    clusters.append([randint(
        55, 745), randint(55, 545)])


def calculate_distance(p1, p2):
    return math.sqrt((pow((p1[0]-p2[0]), 2)+pow((p1[1]-p2[1]), 2)))


while running:
    clock.tick(60)
    screen.fill(BACKGROUND)

    # Draw interface
    # Draw panel
    pygame.draw.rect(screen, BLACK, (50, 50, 700, 500))
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 690, 490))

    # K button +
    pygame.draw.rect(screen, BLACK, (850, 50, 50, 50))
    screen.blit(text_plus, (865, 50))

    # K button -
    pygame.draw.rect(screen, BLACK, (950, 50, 50, 50))
    screen.blit(text_minus, (970, 50))

    # K display
    text_K = font.render("K = "+str(k_count), True, BLACK)
    screen.blit(text_K, (1050, 50))

    # Run button
    pygame.draw.rect(screen, BLACK, (850, 150, 125, 50))
    screen.blit(text_run, (875, 160))

    # Random button
    pygame.draw.rect(screen, BLACK, (850, 250, 125, 50))
    screen.blit(text_random, (850, 260))

    # Error display
    text_error = font.render("Error = " + str(error), True, BLACK)
    screen.blit(text_error, (850, 330))

    # Algorithm button
    pygame.draw.rect(screen, BLACK, (850, 400, 150, 50))
    screen.blit(text_algorithm, (850, 400))

    # Reset button
    pygame.draw.rect(screen, BLACK, (850, 500, 125, 50))
    screen.blit(text_reset, (850, 510))

    # End draw interface

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # show mouse cursor point when in panel
    if 55 < mouse_x < 745 and 55 < mouse_y < 545:
        text_point = smaller_font.render(
            "("+str(mouse_x-55)+","+str(mouse_y-55)+")", True, BLACK)
        screen.blit(text_point, (mouse_x+10, mouse_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            # adding mouse cursor click to points
            if 55 < mouse_x < 745 and 55 < mouse_y < 545:
                if labels != []:
                    labels = []
                else:
                    point = mouse_x, mouse_y
                    points.append(point)
                    pygame.draw.circle(
                        screen, BLACK, (mouse_x-55, mouse_y-55), 2)
                    screen.blit(text_point, (mouse_x+10, mouse_y))
                    print(points)

                # Change K button +
            if 850 < mouse_x < 900 and 50 < mouse_y < 100:
                if k_count >= 6:
                    k_count = 6
                else:
                    k_count = k_count + 1

            # Change K button -
            if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
                if k_count <= 0:
                    k_count = 0
                else:
                    k_count = k_count - 1

            # Run button
            if 850 < mouse_x < 975 and 150 < mouse_y < 200:
                labels = []
                for i in range(len(points)):
                    distances = []
                    for j in range(len(clusters)):
                        # find distance from points to clusters
                        distance = calculate_distance(points[i], clusters[j])
                        distances.append(distance)

                    # find min distance then add it to labels
                    if distances != []:
                        min_distance = min(distances)
                        label_index = distances.index(min_distance)
                        labels.append(label_index)

                # find the x and y of the center for clusters
                for k in range(len(clusters)):
                    avg_x_distance = 0
                    avg_y_distance = 0
                    sum_x_distance = 0
                    sum_y_distance = 0
                    total_error = 0
                    count = 0
                    for m in range(len(points)):
                        if (labels[m] == k):
                            # Sums of error
                            total_error += calculate_distance(
                                points[m], clusters[k])
                            # Sums of x and y
                            sum_x_distance += points[m][0]
                            sum_y_distance += (points[m][1])
                            count += 1
                    if count != 0:
                        avg_x_distance = sum_x_distance/count
                        avg_y_distance = sum_y_distance/count
                        clusters[k] = avg_x_distance, avg_y_distance

                    error = int(total_error)

            # Random button
            if 850 < mouse_x < 975 and 250 < mouse_y < 300:
                labels = []
                clusters = []
                error = 0
                for n in range(k_count):
                    cluster_random()
                    pygame.draw.circle(
                        screen, RED, (clusters[n][0], clusters[n][1]), 8)

           # Algorithm button
            if 850 < mouse_x < 1000 and 400 < mouse_y < 450:
                if k_count != 0:
                    kmeans = KMeans(n_clusters=k_count).fit(points)
                    labels = kmeans.predict(points)
                    clusters = kmeans.cluster_centers_

                # Reset button
            if 850 < mouse_x < 975 and 500 < mouse_y < 550:
                points = []
                clusters = []
                error = 0
                k_count = 0

    for i in range(len(clusters)):
        pygame.draw.circle(screen, COLORS[i],
                           (clusters[i][0], clusters[i][1]), 8)

    for i in range(len(points)):
        pygame.draw.circle(screen, BLACK, (points[i][0], points[i][1]), 6)

        if (len(labels) <= 0):
            pygame.draw.circle(
                screen, WHITE, (points[i][0], points[i][1]), 5)

        else:
            pygame.draw.circle(
                screen, COLORS[labels[i]], (points[i][0], points[i][1]), 5)

    pygame.display.flip()

pygame.quit()
