# Author: Mr0o (https://github.com/Mr0o)
# July 13 2023

# Somewhat boilerplate for using pymunk with pygame
# But also a general demo of pymunk

import pygame
import pymunk

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# for rendering text
font = pygame.font.SysFont("Arial", 16, bold=True)

pygame.display.set_caption("Pymunk Demo")

space = pymunk.Space()
space.gravity = (0.0, 900.0)

# create ball and add it to the pymunk space
def create_ball(space, position):
    # create a dynamic body
    mass = 1
    radius = 14
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.95
    shape.friction = 0.9
    space.add(body, shape)

# create a static body
static_body = pymunk.Body(body_type=pymunk.Body.STATIC)

# create static line segments along the edges of the screen
def create_static_lines(space):
    static_lines = [pymunk.Segment(static_body, (0.0, 0.0), (0.0, HEIGHT - 0.0), 0.0),
                    pymunk.Segment(static_body, (0.0, HEIGHT - 0.0), (WIDTH - 0.0, HEIGHT - 0.0), 0.0),
                    pymunk.Segment(static_body, (WIDTH - 0.0, HEIGHT - 0.0), (WIDTH - 0.0, 0.0), 0.0),
                    pymunk.Segment(static_body, (0.0, 0.0), (WIDTH - 0.0, 0.0), 0.0)]
    for line in static_lines:
        line.elasticity = 0.95
        line.friction = 0.9

    space.add(static_body, *static_lines)

# create the static lines
create_static_lines(space)

# game loop
while True:
    mouseClick = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_SPACE:
                # clear the balls
                space.remove(*space.bodies)
                space.remove(*space.shapes)

                # create the static lines
                create_static_lines(space)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                mouseClick = True

    # create ball on mouse click
    if mouseClick or pygame.mouse.get_pressed()[0]:
        # create a dynamic body at mouse position
        create_ball(space, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

    
    # remove any ball that goes outside the screen
    for ball in space.bodies:
        if ball.position.y < 0 or ball.position.y > HEIGHT or ball.position.x < 0 or ball.position.x > WIDTH:
            space.remove(ball)
        

    screen.fill((255, 255, 255))

    # draw lines
    for line in space.shapes:
        if isinstance(line, pymunk.Segment):
            pygame.draw.line(screen, (0, 0, 0), line.a, line.b, 10)

    # draw circle
    for ball in space.bodies:
        for shape in ball.shapes:
            if isinstance(shape, pymunk.Circle):
                pos = int(ball.position.x), int(ball.position.y)
                pygame.draw.circle(screen, (190, 0, 0), pos, int(shape.radius), 0)

    # update physics
    space.step(clock.get_time() / 1000.0)

    # draw text
    text = font.render("Use left or right mouse click to create a ball", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    text = font.render("Press ESC to quit     Press SPACE to clear the balls", True, (0, 0, 0))
    screen.blit(text, (10, 30))

    # draw some performance metrics
    text = font.render(str(clock.get_rawtime()) + " ms", True, (0, 0, 0))
    screen.blit(text, (10, 50))
    text = font.render("FPS: " + str(int(clock.get_fps())), True, (0, 0, 0))
    screen.blit(text, (10, 70))
    text = font.render("Number of balls: " + str(len(space.bodies)), True, (0, 0, 0))
    screen.blit(text, (10, 90))


    pygame.display.update()
    pygame.display.flip()
    clock.tick(300)



