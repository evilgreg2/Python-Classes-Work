import pygame
import pymunk
from math import degrees


pygame.init()
main_surface = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

ball_img = pygame.image.load("./assets/SoccerBall.png")
bal_img = pygame.transform.scale(ball_img,(30,30))


space = pymunk.Space()
space.gravity = 0, -1000

body = pymunk.Body()
body.position = 250,500

shape = pymunk.Circle(body, 60)
shape.density = 1
shape.elasticity  = 0.7
shape.friction = 1

space.add(body, shape)

body2 = pymunk.Body()
body2.position = 200, 400

shape2 = pymunk.Circle(body2, 20)
shape2.density = 1
shape2.elasticity = 0.8
shape2.friction = 1

space.add(body2, shape2)

floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
floor_body.position = 250,50

floor_shape = pymunk.Segment(floor_body, (-250, 0), (250, 10), 1)
floor_shape.density = 1
floor_shape.elasticity = 0.7
floor_shape.friction = 1

space.add(floor_body,floor_shape)

joint = pymunk.constraints.PinJoint(body, body2, (0,0), (0,0))
space.add(joint)

pin = pymunk.constraints.PivotJoint(body2, space.static_body, (0,0), body2.position)
space.add(pin)

def convert(pos, height):
    x, y = pos
    return x, height - y



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                space.remove(pin)
            if event.key == pygame.K_2:
                space.remove(joint)
          
        
    
    main_surface.fill((255,255,255))
    
    pygame.draw.circle(main_surface, (255,0,0), convert(body2.position, 500), 20)

    #pygame.draw.circle(main_surface, (255, 0, 0), convert(body.position, 500), 30)
    ball_pos = convert(body.position, 500)
    rotated_ball = pygame.transform.rotate(ball_img, degrees(body.angle))
    dest_rect = rotated_ball.get_rect(center = ball_pos)
    main_surface.blit(rotated_ball, dest_rect)


    a = convert(floor_body.local_to_world(floor_shape.a), 500)
    b = convert(floor_body.local_to_world(floor_shape.b), 500)

    pygame.draw.line(main_surface, (0, 0, 0), a, b, 5)


    if joint in space.constraints:
        a = convert(body.position, 500)
        b= convert(body2.position, 500)
        pygame.draw.line(main_surface, (0,0,0), a, b, 6)

    
    pygame.display.update()
    clock.tick(60)
    space.step(1/60)
