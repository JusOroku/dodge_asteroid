import sys, pygame, time, random
size = width, height = 1024, 768
FPS = 60
#load asset
background = pygame.image.load("background/space_background.jpg")
spaceship_sprite = pygame.image.load("sprite/spaceship_sprite.png")
asteroid_sprite = pygame.image.load("sprite/asteroid1.png")
bullet_sprite = pygame.image.load("sprite/bullet1.png")
redColour = pygame.Color(255, 0, 0)

def set_ship_start_position (spaceship):
    spaceship_rect = spaceship.get_rect()
    spaceship_rect.x = width/2 - 64
    spaceship_rect.y = height - 128
    return spaceship_rect

def spaceship_control (spaceship_rect,event,spaceship_speed):
    if event.type == pygame.QUIT:
        sys.exit()

    #spaceship control
    presskey = pygame.key.get_pressed()
    if presskey[pygame.K_LEFT]:
        spaceship_speed[0] = -15
    elif presskey[pygame.K_RIGHT]:
        spaceship_speed[0] = 15
    else:
        spaceship_speed[0] = 0

def shooting_beam(spaceship_rect):
    #shooting a beam
    beam_rect = bullet_sprite.get_rect()
    beam_rect.bottom = spaceship_rect.top
    beam_rect.centerx = spaceship_rect.centerx
    return beam_rect

def bullet_control(bullet_array,bullet_speed,screen):
    bullet_remove_array = []
    for i in range(len(bullet_array)):
        bullet_array[i] = bullet_array[i].move(bullet_speed)
        screen.blit(bullet_sprite,bullet_array[i])
        if (bullet_array[i].bottom) < 0:
            bullet_remove_array.append(i)

    for i in range(len(bullet_remove_array)):
        bullet_array.pop(bullet_remove_array[i])

def asteroid_spawn():

    asteroid_rect = asteroid_sprite.get_rect()
    asteroid_rect.top = 0
    asteroid_rect.centerx = random.randint(0,width)
    return asteroid_rect

def asteroid_control(asteroid_array,asteroid_speed_array,screen,score):
    asteroid_remove_array = []
    for i in range(len(asteroid_array)):
        asteroid_array[i] = asteroid_array[i].move(asteroid_speed_array[i])
        screen.blit(asteroid_sprite,asteroid_array[i])
        if (asteroid_array[i].top > height):
            asteroid_remove_array.append(i)
    for i in range(len(asteroid_remove_array)):
        asteroid_array.pop(asteroid_remove_array[i])
        asteroid_speed_array.pop(asteroid_remove_array[i])
        score[0] = score[0] + 1


# def bullet_asteroid_collision(bullet_array, asteroid_array, asteroid_speed_array):
#     bullet_collide_array = []
#     asteroid_collide_array = []
#     for i in range(len(bullet_array)):
#         for j in range(len(asteroid_array)):
#             if bullet_array[i].colliderect(asteroid_array[j]):
#                 bullet_collide_array.append(i)
#                 asteroid_collide_array.append(j)
#
#     #bullet_collide_array = sorted(bullet_collide_array, key = lambda x:(-x))
#     #asteroid_collide_array = sorted(asteroid_collide_array,  key = lambda x:(-x))
#     print asteroid_collide_array
#     for i in range(len(bullet_collide_array)):
#         bullet_array.pop(bullet_collide_array[i])
#     for i in range(len(asteroid_collide_array)):
#         asteroid_array.pop(asteroid_collide_array[i])
#         asteroid_speed_array.pop(asteroid_collide_array[i])


def main():
    score = [0]
    redColour = pygame.Color(255, 0, 0)
    pygame.init()
    screen = pygame.display.set_mode(size)
    spaceship_rect = set_ship_start_position(spaceship_sprite)
    spaceship_speed = [0,0]
    bullet_speed = [0,-10]
    bullet_array = []
    asteroid_array = []
    asteroid_speed_array = []
    asteroid_spawn_counter = 0
    score_font = pygame.font.Font(None, 40)
    while 1:

        scoreSurf = score_font.render('Score: ' + str(score[0]), True, redColour)
        scoreRect = scoreSurf.get_rect()
        scoreRect.midtop = (70, 20)


        for event in pygame.event.get():
            spaceship_control(spaceship_rect,event, spaceship_speed)
        spaceship_rect = spaceship_rect.move(spaceship_speed)
        if spaceship_rect.left < 0:
            spaceship_rect.left = 0
        if spaceship_rect.right > width:
            spaceship_rect.right = width

        screen.blit(background, [0,0])
        screen.blit(spaceship_sprite, spaceship_rect)
        screen.blit(scoreSurf, scoreRect)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                main()
            #if event.key == pygame.K_SPACE and len(bullet_array) <= 50:
                #bullet_rect = shooting_beam(spaceship_rect)
                #bullet_array.append(bullet_rect)

        #bullet_control(bullet_array,bullet_speed,screen)
        asteroid_spawn_seed = random.randint(5,40)
        if (asteroid_spawn_counter > asteroid_spawn_seed):
            asteroid_spawn_seed = random.randint(5,20)
            asteroid_spawn_counter = 0
            asteroid_rect = asteroid_spawn()
            asteroid_array.append(asteroid_rect)
            asteroid_y_speed = random.randint(10,20)
            asteroid_speed_array.append([0,asteroid_y_speed])

        asteroid_control(asteroid_array,asteroid_speed_array,screen, score)

        asteroid_spawn_counter += 1
        #bullet_asteroid_collision(bullet_array, asteroid_array, asteroid_speed_array)
        for i in(range(len(asteroid_array))):
            if spaceship_rect.colliderect(asteroid_array[i]):
                print "Collide"
                gameover(score)
        pygame.display.flip()

def gameover(score):
    redColour = pygame.Color(255, 0, 0)
    pygame.init()
    screen = pygame.display.set_mode(size)
    gameOverFont = pygame.font.Font(None, 80)
    gameOverSurf = gameOverFont.render('Game Over, Press R to restart', True, redColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (width/2-50, height/2-50)
    scoreSurf = gameOverFont.render('Your score = ' + str(score[0]),True,redColour)
    scoreRect = scoreSurf.get_rect()
    scoreRect.midtop = ((width/2+50, height/2+50))
    while 1:
        screen.blit(gameOverSurf, gameOverRect)
        screen.blit(scoreSurf, scoreRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
        pygame.display.flip()

main()
