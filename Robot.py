import pygame

from random import randint

pygame.init()
main_surface = pygame.display.set_mode((700,700))

clock = pygame.time.Clock()
robot_x = 350
robot_y = 350
robot_angle = 0

robot_surface = pygame.Surface((50,50))
pygame.draw.circle(robot_surface, (150,150,150), (25,25), 25)

pygame.draw.circle(robot_surface, (50,50,50), (40,25), 7)
robot_surface.set_colorkey((0,0,0))
robot_rect = robot_surface.get_rect()


wall_rect = pygame.Rect((50,50), (400,5))

walls = (
    pygame.Rect((50 , 50), (400 , 5)),
    pygame.Rect((450 , 50), (5 , 200)),
    pygame.Rect((450 , 250), (100 , 5)),
    pygame.Rect((545 , 255), (5 , 300)),
    pygame.Rect((50 , 550), (495 , 5)),
    pygame.Rect((50 , 50 ), (5 , 500)),
    
)

dust_surface = pygame.Surface((500,500))
dust_surface.fill((255, 255, 255))

dust_amount = 0
while dust_amount < 1000:
    dust_x = randint(0, 500)
    dust_y = randint(0, 500)
    pygame.draw.circle(dust_surface, (0,0,0), (dust_x, dust_y), 3)
    dust_amount += 1

mask = pygame.Rect((405,0), (100,200))
pygame.draw.rect(dust_surface, (255,255,255), mask)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    pressed = pygame.key.get_pressed()
    delta_x , delta_y = 0 , 0

    if pressed[pygame.K_w]:
        delta_y -= 3
        robot_angle = 90
    if pressed[pygame.K_s]:
        delta_y  +=3
        robot_angle = 270
    if pressed[pygame.K_a]:
        delta_x -= 3
        robot_angle = 180
    if pressed[pygame.K_d]:
        delta_x += 3
        robot_angle = 0
   
    robot_rect.top += delta_y
    robot_rect.left += delta_x


    for wall in walls: 
        if robot_rect.colliderect(wall):
            delta_x, delta_y = 0, 0
    
    robot_x += delta_x
    robot_y += delta_y


    main_surface.fill((255,255,255))
    main_surface.blit(dust_surface, (50,50))



    for wall in walls:
        pygame.draw.rect(main_surface, (0,0,0), wall)


    rotated_robot_surface = pygame.transform.rotate(robot_surface, robot_angle)
    robot_rect = main_surface.blit(rotated_robot_surface, (robot_x,robot_y))

    pygame.draw.rect(dust_surface, (255,255,255), robot_rect.move(-50,-50))

    pygame.display.update()
    clock.tick(60)