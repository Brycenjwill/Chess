import pygame
WIDTH = 500
HEIGHT = 600
WHITE = pygame.Color("#f8f3f1")
BLACK = pygame.Color("#4e3023")
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("tan")

    # RENDER YOUR GAME HERE
    #Draw board squares
    posx = 50
    posy = 100
    row = 0
    for i in range(64):
        if row % 2 == 0:
            if i % 2 == 0:
                pygame.draw.rect(screen, WHITE, pygame.Rect(posx, posy, 50, 50))
            else: 
                pygame.draw.rect(screen, BLACK, pygame.Rect(posx, posy, 50, 50))
        else:
            if i % 2 == 0:
                pygame.draw.rect(screen, BLACK, pygame.Rect(posx, posy, 50, 50))
            else: 
                pygame.draw.rect(screen, WHITE, pygame.Rect(posx, posy, 50, 50))
        if posx == 400:
            posy += 50
            posx = 50
            row += 1
        else:
            posx += 50


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()