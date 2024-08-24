import pygame
import pymunk

pygame.init()

main_surface = pygame.display.set_mode((800,700))
clock = pygame.time.Clock()


space = pymunk.Space()
space.gravity = (0, -1000)

def convert(pos):
    return pos[0], main_surface.get_height() - pos[1]


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

class Rectangle:
    def __init__(self, pos, size, color = (0,0,0), outline = 2) -> None:
        self.color = color
        self.outline = outline
        self.body = pymunk.Body()
        self.body.position = convert(pos)
        verts = (
            (-size[0]/2, -size[1]/2),
            (size[0]/2,  -size[1]/2),
            (size[0]/2, size[1]/2),
            (-size[0]/2, size[1]/2)
        )     

        self.shape = pymunk.Poly(self.body, verts)
        self.shape.density = 1
        self.shape.friction = 0.95
        self.shape.elasticity = 0.3
        space.add(self.body, self.shape) 

    def draw(self):
        points = []
        for v in self.shape.get_vertices():
            world_v = self.body.local_to_world(v)
            pygame_v = convert(world_v)
            points.append(pygame_v)
        pygame.draw.polygon(main_surface,self.color, points, self.outline)

floor = Floor((0,600), (800, 600))

base = Rectangle((400,535), (50,150), color = (144,238,144), outline = 0)
base.body.body_type = pymunk.Body.STATIC

arm = Rectangle((400,450), (400,20), color = (135,206,250), outline = 0)


base.shape.filter = pymunk.ShapeFilter(group=1)

arm.shape.filter = pymunk.ShapeFilter(group=1)

nail1 = pymunk.PivotJoint(base.body, arm.body, (0, 65), (0,0))
space.add(nail1)

weight = Rectangle((600,100), (100,100), color = (255,182,193), outline = 0)
weight.body.mass = 60000
obj1 = Rectangle((210, 440), (30,30), color = (240,128,128), outline = 0)

support = Rectangle((200,525), (50,115), color = (255,204,153), outline = 0)


moving_body = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for shape in space.shapes:
                if shape.body.body_type == pymunk.Body.STATIC:
                    continue
                if shape.body == arm.body:
                    continue
                if shape.bb.contains_vect(convert(event.pos)):
                    shape.body.body_type = pymunk.Body.KINEMATIC
                    moving_body = shape.body
                    print(shape.body)
        if event.type == pygame.MOUSEBUTTONUP:
            if moving_body is not None:
                moving_body.body_type = pymunk.Body.DYNAMIC
                moving_body = None
        if event.type == pygame.MOUSEMOTION:
            if moving_body is not None:
                moving_body.position = convert(event.pos)

    main_surface.fill((255, 255, 255))
    floor.draw()
    base.draw()
    arm.draw()
    weight.draw()
    obj1.draw()
    support.draw()

    pygame.display.update()
    clock.tick(60)
    space.step(1/60)