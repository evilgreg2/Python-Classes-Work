import pygame


from random import randint

pygame.init()

main_surface = pygame.display.set_mode((700,700))
clock = pygame.time.Clock()


bg = pygame.image.load("./assets/Background.png")

pop_sound = pygame.mixer.Sound("./assets/pop.ogg")

bad_sound = pygame.mixer.Sound("./assets/bad.wav")

score_font = pygame.font.Font("./assets/pixel.ttf", 28)

bomb_img = pygame.image.load("./assets/bomb.png")
bomb_img = pygame.transform.scale(bomb_img, (75,75))

explosion_sound = pygame.mixer.Sound("./assets/explosion.flac")

explosion_tiles = pygame.image.load("./assets/explosion_tiles.png")

def load_balloons():
    colors = ["black", "blue", "green", "red"]
    result = []
    for c in colors:
        img_name = "./assets/balloon_" + c + ".png"
        img = pygame.image.load(img_name)
        scaled_img = pygame.transform.scale(img, (60,75))
        result.append(scaled_img)
    return result

def spawn_bubble():
    x = randint(0,650)
    y = randint(-100,20)
    kind = randint(0,3)
    return [x, y, kind]

def spawn_bomb():
    x = randint(0,650)
    y = randint(-100,20)
    return [x,y]





balloon_imgs = load_balloons()

bubbles = [spawn_bubble() for _ in range(5)]
bombs = [spawn_bomb() for _ in range(2)]




pop_events = []
explosion_events = []

score = 0

def pop_balloon(click_pos):
    global score
    for b  in bubbles:
        bx , by, *_ = b
        brect = pygame.Rect((bx, by), (60,75))

        if brect.collidepoint(click_pos):
            bubbles.remove(b)
            pop_sound.play()
            score += 2
            add_pop_event(click_pos, "+2")

def explode(click_pos):
    global score
    for b in bombs:
        bx, by = b
        brect = pygame.Rect((bx,by), bomb_img.get_size())
        if brect.collidepoint(click_pos):
            bombs.remove(b)
            score -= 10
            add_pop_event(click_pos, "-10")
            explosion_sound.play()
            explosion_events.append([click_pos[0], click_pos[1], 0])


def add_pop_event(pos, text):
    img = score_font.render(text, True, (255,255,255))
    x, y = pos

    pop_events.append([x, y, img, 60])


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pop_balloon(event.pos)
            explode(event.pos)

    main_surface.blit(bg, (0,0))
    for b in bubbles:
        main_surface.blit(balloon_imgs[b[2]], (b[0], b[1]))
        b[1] += 2

    if randint(0,20) == 0 :
        bubbles.append(spawn_bubble())

    if randint(0,60) == 0 :
        bombs.append(spawn_bomb())
    
    score_img = score_font.render(
        "Score: " + str(score), True,(255,255,255)
    )

    main_surface.blit(score_img, (0,0))

    for b in bubbles:
        if b[1] > main_surface.get_height():
            score -= 5
            add_pop_event((b[0], b[1]), "-5")
            bad_sound.play()
            bubbles.remove(b)
    
    for b in bombs:
        main_surface.blit(bomb_img, b)
        b[1] += 4
    
    for e in pop_events:
        if e[3] ==0:
            pop_events.remove(e)
        e[1] -= 2
        e[3] -= 1
        main_surface.blit(e[2], (e[0], e[1]))

    for ee in explosion_events:
        x, y, frame = ee
        crop_x = (frame % 8) * 256
        crop_y = (frame // 8) * 256
        crop_rect = pygame.Rect((crop_x, crop_y), (256,256))
        main_surface.blit(explosion_tiles, (x - 256/2 , y - 256/2), crop_rect)
        ee[2] += 1
        if frame > 63:
            explosion_events.remove(ee)


    pygame.display.update()
    clock.tick(60)

