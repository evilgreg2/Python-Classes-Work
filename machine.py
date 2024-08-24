import pygame
import pymunk
from math import degrees
from random import randint

pygame.init()
main_surface = pygame.display.set_mode((1000,700))
clock = pygame.time.Clock()


# Pymunk initlization
space = pymunk.Space()
space.gravity = (0,-1000)

def convert(pos):
    height = main_surface.get_height()
    return int(pos[0]), height - int(pos[1])


# Running mainloop

class Floor:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.body.position = convert(a)
        local_b = self.body.world_to_local(convert(b))
        self.shape = pymunk.Segment(self.body, (0 , 0), local_b, 5)
        self.shape.density = 1
        self.shape.friction = 0.95
        space.add(self.body, self.shape)

    def draw(self):
        a = self.body.local_to_world(self.shape.a)
        b = self.body.local_to_world(self.shape.b)
        pygame.draw.line(
            main_surface,
            (0,0,0),
            convert(a),
            convert(b),
            int(self.shape.radius),        
        )

class Frame:
    def __init__(self, pos, size) -> None:
        self.body = pymunk.Body()
        self.body.position = pos
        verts = (
            (-size[0]/2, 0),
            (size[0]/2, 0),
            (size[0]/2, size[1]),
            (-size[0]/2, size[1])
        )     

        self.shape = pymunk.Poly(self.body, verts)
        self.shape.density = 1
        space.add(self.body, self.shape) 

    def draw(self):
        points = []
        for v in self.shape.get_vertices():
            world_v = self.body.local_to_world(v)
            pygame_v = convert(world_v)
            points.append(pygame_v)
        pygame.draw.polygon(main_surface,(0,0,0), points, 2)


class Wheel:
    def __init__(self, pos, radius) -> None:
        self.body = pymunk.Body()
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = 1
        self.shape.friction = 0.95
        space.add(self.body, self.shape)
        self.img = pygame.image.load("./assets/SoccerBall2.png")
        self.img = pygame.transform.scale(self.img, (2 * radius, 2 * radius))

    def draw(self):
        rotated_img = pygame.transform.rotate(
            self.img, degrees(self.body.angle))

        dest = rotated_img.get_rect(center=convert(self.body.position))
        main_surface.blit(rotated_img,dest) 

        # pygame.draw.circle(
         #   main_surface,
         #   (0,0,0),
         #   convert(self.body.position),
         #   self.shape.radius,
        
       # )

#floor = Floor((0, 650), (30, 550))

floor_segments = []
for i in range(20):
    last_segment_b = (0,650)
    if len(floor_segments) > 0:
        last_segment_b = floor_segments[-1].b
    a = last_segment_b
    b = (last_segment_b[0] + 50, randint(610, 650))
    floor_segments.append(Floor(a, b))



frame = Frame((500, 150), (200, 50))
wheel1 = Wheel((400, 100), 30)
wheel2 = Wheel((600,100), 30)


rear_arm = pymunk.PinJoint(
    wheel1.body,
    frame.body,
    (0,0),
    (-400, 0),
)
space.add(rear_arm)

front_arm = pymunk.PinJoint(
    wheel2.body,
    frame.body,
    (0,0),
    (400, 0),
)
space.add(front_arm)

motor = pymunk.SimpleMotor(
    wheel1.body,
    frame.body,
    0,
)
space.add(motor)


wd4 = pymunk.GearJoint(
    wheel1.body,
    wheel2.body,
    0, 1
)
space.add(wd4)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                motor.rate += 4
            if event.key == pygame.K_d:
                motor.rate -= 4
            if event.key == pygame.K_SPACE:
                motor.rate *= 3
        if event.type == pygame.KEYUP:
           motor.rate = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
           space.remove(wd4)
        if event.type == pygame.MOUSEBUTTONUP:
           space.add(wd4)  



    main_surface.fill((255,255,255))

    for seg in floor_segments:
        seg.draw()
    
    frame.draw()
    wheel1.draw()
    wheel2.draw()

    pygame.display.update()
    clock.tick(60)
    space.step(1/60)