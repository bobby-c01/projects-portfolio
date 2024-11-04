
import pygame
import pymunk
import pymunk.pygame_util
import math
import time
pygame.init()

WIDTH, HEIGHT = 900, 500
ANGLE, SPEED = 1, 700
PLAYER_COLLISION_TYPE = 1
PROJECTILE_COLLISION_TYPE = 2
PLAYSIZE = 20
DELAY = 2.0
display = pygame.display.set_mode((WIDTH, HEIGHT))

def handle_collision(players):
    def callback(arbiter, space, data):
        shape_a, shape_b = arbiter.shapes

       
        if shape_a.collision_type == PLAYER_COLLISION_TYPE:
            player_shape = shape_a
            projectile_shape = shape_b
        else:
            player_shape = shape_b
            projectile_shape = shape_a

    
        for player in players:
            if player['shape'] == player_shape:
                player['health'] -= 1
                print(f"Player hit! Health is now {player['health']}")

              
                if player['health'] <= 0:
                    print("Player has been defeated!")

 
        space.remove(projectile_shape, projectile_shape.body)
        return True

    return callback

def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def draw(space, display, draw_options, players):
    display.fill("white")
    space.debug_draw(draw_options)
    for player in players:
        pygame.draw.rect(display, player['color'], (player['body'].position[0] - PLAYSIZE // 2, player['body'].position[1] - PLAYSIZE // 2, PLAYSIZE, PLAYSIZE))
    pygame.display.update()

def create_boundaries(space, width, height):
    rects = [
        [(width / 2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
        [(10, height / 2), (20, height)],
        [(width - 10, height / 2), (20, height)]
    ]
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)

def create_player(space, position, color):
    mass = 100
    size = (PLAYSIZE, PLAYSIZE)
    inertia = pymunk.moment_for_box(mass, size)
    body = pymunk.Body(mass, inertia, pymunk.Body.KINEMATIC)
    body.position = position
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = 0.4
    shape.friction = 0.5
    shape.collision_type = PLAYER_COLLISION_TYPE
    space.add(body, shape)
    return {'body': body, 'shape': shape, 'color': color, 'health': 3}

def create_structure(space):
    BROWN = (139, 69, 19, 100)
    rects = [
        [(440, 380), (20, 200), BROWN, 10000],

    ]
    for pos, size, color, mass in rects:
        body = pymunk.Body(mass, pymunk.moment_for_box(mass, size))
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.color = color
        shape.elasticity = 1
        shape.friction = 0.9
        space.add(body, shape)

def create_projectile(space, position, velocity):
    mass = 10
    radius = 5
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = position
    body.velocity = velocity
    shape = pymunk.Circle(body, radius)
    shape.collision_type = PROJECTILE_COLLISION_TYPE
    shape.elasticity = 0.9
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape

def angle_speed_to_velocity(angle, speed):
    radians = math.radians(angle)
    vx = speed * math.cos(radians)
    vy = speed * math.sin(radians)
    return vx, -vy

def display_text(display, text, position):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(str(text), True, (0, 0, 0))
    display.blit(text_surface, position)

def main(display, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 781)

    create_boundaries(space, width, height)
    create_structure(space)

    draw_options = pymunk.pygame_util.DrawOptions(display)

    player1 = create_player(space, (width // 2 - 100, height - PLAYSIZE - 20), (255, 0, 0))
    player2 = create_player(space, (width // 2 + 90, height - PLAYSIZE - 20), (0, 0, 255))

    players = [player1, player2]

    handler = space.add_collision_handler(PLAYER_COLLISION_TYPE, PROJECTILE_COLLISION_TYPE)
    handler.begin = handle_collision(players)

    player1_angle = 90
    player1_speed = 5
    player1_can_shoot = True

    player2_angle = 90
    player2_speed = player1_speed
    player2_can_shoot = True

    time1 = time.time()
    time2 = time.time()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_l:
                    player1_can_shoot = True
                elif event.key == pygame.K_g:
                    player2_can_shoot = True
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player1['body'].position = (player1['body'].position[0] - player1_speed, player1['body'].position[1])
        if keys[pygame.K_RIGHT]:
            player1['body'].position = (player1['body'].position[0] + player1_speed, player1['body'].position[1])
        if keys[pygame.K_UP]:
            player1_angle -= ANGLE
        if keys[pygame.K_DOWN]:
            player1_angle += ANGLE
        if keys[pygame.K_l] and ((time.time() - time1) > DELAY) and player1_can_shoot:
            time1 = time.time()
            vx, vy = angle_speed_to_velocity(player1_angle, SPEED)
            create_projectile(space, (player1['body'].position[0] + PLAYSIZE * 0.75, player1['body'].position[1] - PLAYSIZE * 0.5), (vx, vy))
            player1_can_shoot = False

        if keys[pygame.K_a]:
            player2['body'].position = (player2['body'].position[0] - player2_speed, player2['body'].position[1])
        if keys[pygame.K_d]:
            player2['body'].position = (player2['body'].position[0] + player2_speed, player2['body'].position[1])
        if keys[pygame.K_w]:
            player2_angle -= ANGLE
        if keys[pygame.K_s]:
            player2_angle += ANGLE
        if keys[pygame.K_g] and player2_can_shoot and ((time.time() - time2) > DELAY):
            time2 = time.time()
            vx, vy = angle_speed_to_velocity(player2_angle, SPEED)
            create_projectile(space, (player2['body'].position[0] - PLAYSIZE * 0.25, player2['body'].position[1] - PLAYSIZE * 0.5), (vx, vy))
            player2_can_shoot = False

        player1['body'].position = (max(0, min(player1['body'].position[0], WIDTH - PLAYSIZE)), max(0, min(player1['body'].position[1], HEIGHT - PLAYSIZE)))
        player2['body'].position = (max(0, min(player2['body'].position[0], WIDTH - PLAYSIZE)), max(0, min(player2['body'].position[1], HEIGHT - PLAYSIZE)))

        space.step(dt)

        draw(space, display, draw_options, players)

      
        display_text(display, player1['health'], (40, 25))
        display_text(display, player2['health'], (WIDTH - 80, 25))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main(display, WIDTH, HEIGHT)
