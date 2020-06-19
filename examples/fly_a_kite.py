import pygame
from pygame.locals import (
    K_ESCAPE,
    K_RIGHT,
    K_LEFT,
    K_s,
    K_p,
    K_f,
    KEYDOWN,
    QUIT,
)

import flight
import physics
from examples.sprites.kite_sprite import KiteSprite
from flight.kites.bridle import Bridle
import display


def run_game():

    clock = pygame.time.Clock()
    running = True
    paused = False
    show_forces = True

    target_steps = 500
    fps = 30
    spf = int(target_steps/fps)
    t = 1.0/target_steps

    while running:
        step = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RIGHT:
                    atmosphere.wind_speed = \
                        atmosphere.wind_speed.add(physics.Vector2D(-.5, 0))
                if event.key == K_LEFT:
                    atmosphere.wind_speed = \
                        atmosphere.wind_speed.add(physics.Vector2D(.5, 0))
                if event.key == K_f:
                    show_forces = not show_forces
                if event.key == K_s:
                    step = True
                if event.key == K_p:
                    paused = not paused
            elif event.type == QUIT:
                running = False

        if not running:
            break

        screen.fill(pygame.Color("skyblue"))

        pygame.draw.circle(
            screen, pygame.Color("red"),
            projector.project(anchor_position),
            5, 3)

        if step or not paused:

            kite_sprite.update()
            screen.blit(kite_sprite.image, kite_sprite.rect)

            simulator.add_forces()

            if show_forces:
                debug_draw.draw_forces(kite)

            pygame.draw.line(
                screen, pygame.Color("white"),
                projector.project(anchor_position),
                projector.project(kite.global_bridle()),
                1)

            wind_speed_text = font.render(
                'Windspeed: ' + str(atmosphere.wind_speed),
                False, (0, 0, 0))

            lift = kite.total_lift().magnitude()
            drag = kite.total_drag().magnitude()
            l_d = 0
            if drag > 0:
                l_d = lift / drag

            lift_drag_text = font.render(
                'L/D: ' + str(round(l_d, 2)),
                False, (0, 0, 0))

            kite_relative = kite.global_bridle().subtract(anchor_position)
            angle = kite_relative.angle()
            degrees = 180 - angle.degrees()
            if degrees < 0:
                degrees = 0

            angle_text = font.render(
                'Angle: ' + str(round(degrees, 2)),
                False, (0, 0, 0))

            screen.blit(wind_speed_text, (10, 10))
            screen.blit(lift_drag_text, (10, 50))
            screen.blit(angle_text, (10, 90))

            pygame.display.flip()
            simulator.apply_forces(t)

            for i in range(0, spf - 1):
                simulator.step(t)

            clock.tick(fps)


pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wind Tunnel")

anchor_position = physics.Vector2D(0, 3)

projector = display.Projector(physics.Vector2D(
    SCREEN_WIDTH, SCREEN_HEIGHT))

debug_draw = display.DebugDraw(screen, projector)

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

atmosphere = flight.Atmosphere()
atmosphere.wind_speed = physics.Vector2D(-1, 0)

bridle = Bridle(4.1, 3.7, 4)
bridle.initial_pos = anchor_position.subtract(physics.Vector2D(2, 0))

kite = flight.kites.BoxKite(
    4, 2, 4/3.0, atmosphere,
    bridle=bridle,
    initial_orientation=physics.Angle(0))

kite_sprite = KiteSprite(kite, "examples/images/box_kite_big.png", projector)
all_sprites = pygame.sprite.Group()
all_sprites.add(kite_sprite)
projector.set_resolution(kite_sprite.rect.width, 4)
projector.center_x(kite.position())

simulator = flight.Simulator()
simulator.register_flying_object(kite)

anchor = flight.StationaryObject(anchor_position)
simulator.register_stationary_object(anchor, anchor_position)
simulator.tether(
    kite, anchor, kite.bridle_position,
    physics.Vector2D(0, 0), 2)

run_game()
pygame.quit()
