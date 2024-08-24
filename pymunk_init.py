import pygame
import pymunk

pygame.init()

main_surface = pygame.display.set_mode((800,700))
clock = pygame.time.Clock()


space = pymunk.Space()
space.gravity = (0, -1000)

def convert(pos):
    return pos[0], maing_surface.get_height() - pos[1]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    

    main_surface.fill((255, 255, 255))

    pygame.display.update()
    clock.tick(60)
    space.step(1/60)