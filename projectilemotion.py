import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Motion Simulator")


def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)


def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def draw(space, window, draw_options, line):
    window.fill("white")
    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)
    space.debug_draw(draw_options)
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


def create_ground(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (WIDTH / 2, HEIGHT - 10)
    shape = pymunk.Segment(body, (-WIDTH / 2, 0), (WIDTH / 2, 0), 5)
    shape.elasticity = 0.4
    space.friction = 0.5
    space.add(body, shape)
    return body, shape


def create_structure(space):
    BROWN = (139, 69, 19, 100)
    rects = [
        [(600, HEIGHT - 120), (40, 200), BROWN, 100],
        [(900, HEIGHT - 120), (40, 200), BROWN, 100],
        [(750, HEIGHT - 240), (340, 40), BROWN, 150]
    ]
    for pos, size, color, mass in rects:
        body = pymunk.Body(mass, pymunk.moment_for_box(mass, size))
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.color = color
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)


def create_projectile(space, position, velocity):
    mass = 10
    radius = 20
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = position
    body.velocity = velocity
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.4
    space.friction = 0.5
    space.add(body, shape)
    return body, shape


def angle_speed_to_velocity(angle, speed):
    radians = math.radians(angle)
    vx = speed * math.cos(radians)
    vy = speed * math.sin(radians)
    return vx, -vy


def display_text(display, text, position):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (0, 0, 0))
    display.blit(text_surface, position)


def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 981)

    create_boundaries(space, width, height)
    create_ground(space)
    create_structure(space)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    launch_speed = 350
    launch_angle = 50

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                vx, vy = angle_speed_to_velocity(launch_angle, launch_speed)
                if not (math.isnan(vx) or math.isnan(vy)):
                    projectile_body, _ = create_projectile(space, (mouse_x, mouse_y), (vx, vy))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    launch_angle += 5
                elif event.key == pygame.K_DOWN:
                    launch_angle -= 5
                elif event.key == pygame.K_RIGHT:
                    launch_speed += 10
                elif event.key == pygame.K_LEFT:
                    launch_speed -= 10

        window.fill((255, 255, 255))
        space.debug_draw(draw_options)
        display_text(window, f"Angle: {launch_angle}°", (10, 10))
        display_text(window, f"Speed: {launch_speed} m/s", (10, 40))
        display_text(window, f"Up/Down Arrows = adjust angle", (200, 200))
        display_text(window, f"Left/Right Arrows = adjust speed", (200, 250))
        space.step(dt)
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
