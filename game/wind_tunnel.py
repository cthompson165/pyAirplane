import pygame
from pygame.locals import (
    K_ESCAPE,
    K_RIGHT,
    K_LEFT,
    K_s,
    K_p,
    KEYDOWN,
    QUIT,
)

from aerodynamics.simulator import Simulator
from game.kite.surfaceless_kite import SurfacelessKite
from game.enums.colors import Colors
from physics.stationary_object import StationaryObject
from physics.atmosphere import Atmosphere
from util.vector_2d import Vector2D
from util.angle import Angle
from projector import Projector
from debug_draw import DebugDraw
from game.sprites.kite_sprite import KiteSprite


def run_game():

    clock = pygame.time.Clock()
    running = True
    paused = False
    show_forces = True

    while running:
        step = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RIGHT:
                    atmosphere.wind_speed = \
                        atmosphere.wind_speed.add(Vector2D(-.5, 0))
                if event.key == K_LEFT:
                    atmosphere.wind_speed = \
                        atmosphere.wind_speed.add(Vector2D(.5, 0))
                if event.key == K_s:
                    step = True
                if event.key == K_p:
                    paused = not paused
            elif event.type == QUIT:
                running = False

        if not running:
            break

        screen.fill(Colors.SKYBLUE)

        pygame.draw.circle(
            screen, Colors.RED,
            projector.project(anchor_position).array(),
            5, 3)

        if step or not paused:

            kite_sprite.update()
            screen.blit(kite_sprite.image, kite_sprite.rect)

            simulator.add_forces()

            if show_forces:
                debug_draw.draw_forces(kite)

            global_bridle = kite.position().add(
                bridle_position.rotate(
                    kite.orientation()))

            pygame.draw.line(
                screen, Colors.WHITE,
                projector.project(anchor_position).array(),
                projector.project(global_bridle).array(),
                1)

            text_surface = font.render(
                'Windspeed: ' + str(atmosphere.wind_speed),
                False, (0, 0, 0))

            screen.blit(text_surface, (10, 10))

            pygame.display.flip()
            simulator.apply_forces(1/30.0)
            clock.tick(30)


pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wind Tunnel")

anchor_position = Vector2D(0, 5)
kite_position = anchor_position.subtract(Vector2D(1, -1))

projector = Projector(Vector2D(
    SCREEN_WIDTH, SCREEN_HEIGHT))

debug_draw = DebugDraw(screen, projector)

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

atmosphere = Atmosphere()

kite = SurfacelessKite(
    4, 2, atmosphere,
    kite_position, Angle(0))

kite_sprite = KiteSprite(kite, "game/images/box_kite_big.png", projector)
all_sprites = pygame.sprite.Group()
all_sprites.add(kite_sprite)
projector.set_meters_per_pixel(kite_sprite.get_meters_per_pixel(4))
projector.center_x(kite.position())

simulator = Simulator()
simulator.register_flying_object(kite)

bridle_position = Vector2D(1, -1)
anchor = StationaryObject(anchor_position)
simulator.register_stationary_object(anchor, anchor_position)
simulator.tether(
    kite, anchor, bridle_position,
    Vector2D(0, 0), 2)

run_game()
pygame.quit()
