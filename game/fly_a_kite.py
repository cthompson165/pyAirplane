# TODO
# * when cut string need to move center of gravity back to CG
# * move cp to middle as aoa gets larger (middle at 90, 1/4 at 45)

import pygame
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    K_SPACE,
    K_RIGHT,
    K_LEFT,
    K_s,
    K_f,
    K_p,
    KEYDOWN,
    QUIT,
)

from aerodynamics.simulator import Simulator
from game.kite.box_kite import BoxKite
from game.sprites.explosion import Explosion
from game.enums.colors import Colors
from physics.stationary_object import StationaryObject
from util.vector_2d import Vector2D
from util.angle import Angle
from projector import Projector


class Kite(pygame.sprite.Sprite):

    def __init__(self):
        super(Kite, self).__init__()
        self.original_image = pygame.image.load("images/box_kite.png")
        self.image = self.original_image
        self.image.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.image.get_rect(
            center=(
                200, 200
            ))

        self.kite = BoxKite(10, .7, .35, .175, .8, .55, initial_pos, Angle(30))
        self.dead = False

        projector.center_x(self.kite.pos())

    def update(self):
        pos = self.kite.pos()

        screen_pos = projector.project(pos)

        self.image = pygame.transform.rotate(
            self.original_image, self.kite.orientation().degrees())

        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = screen_pos.toint().array()

        if (screen_pos.y >= (SCREEN_HEIGHT - GROUND_HEIGHT - 20)):
            self.kill()
            self.dead = True
            x_pos = int(round(screen_pos.x, 0))
            y_pos = SCREEN_HEIGHT - GROUND_HEIGHT
            expl = Explosion((x_pos, y_pos), 'sm')
            all_sprites.add(expl)
            explosions.add(expl)
            pygame.time.set_timer(GAME_OVER, 1000)
            simulator.unregister(kite.kite)


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
                if event.key == K_SPACE:
                    global string
                    simulator.untether(kite.kite)
                    simulator.atmosphere.wind_speed = Vector2D(0, 0)
                if event.key == K_RIGHT:
                    simulator.atmosphere.wind_speed = \
                            simulator.atmosphere.wind_speed.add(
                                Vector2D(-1, 0))
                if event.key == K_LEFT:
                    simulator.atmosphere.wind_speed = \
                            simulator.atmosphere.wind_speed.add(Vector2D(1, 0))
                if event.key == K_s:
                    step = True
                if event.key == K_p:
                    paused = not paused
                if event.key == K_f:
                    show_forces = not show_forces
            elif event.type == QUIT or event.type == GAME_OVER:
                running = False

        if not running:
            break

        screen.fill(Colors.SKYBLUE)

        pygame.draw.rect(screen,
                         Colors.FOREST_GREEN,
                         (0, SCREEN_HEIGHT - GROUND_HEIGHT,
                          SCREEN_WIDTH, GROUND_HEIGHT))

        origin = projector.project(Vector2D(0, 0))

        pygame.draw.circle(
            screen, Colors.RED,
            (int(origin.x), int(origin.y)), 5, 3)

        explosions.update()
        for explosion in explosions:
            screen.blit(explosion.image, explosion.rect)

        if step or not paused:
            simulator.add_forces()

            if not kite.dead:
                kite.update()
                screen.blit(kite.image, kite.rect)

            if show_forces:
                surface_forces = kite.kite.local_forces()
                for force in surface_forces:
                    global_force = force.local_to_global(
                        kite.kite.pos(), kite.kite.orientation())
                    start_pos = projector.project(global_force.pos)
                    end_pos = projector.project(global_force.endpoint())

                    pygame.draw.line(
                        screen, Colors.RED,
                        start_pos.array(), end_pos.array(), 2)

                airspeed = kite.kite.airspeed()
                pos = kite.kite.pos()
                end_pos = pos.add(airspeed)

                pygame.draw.line(
                        screen, Colors.GREEN,
                        projector.project(pos).array(),
                        projector.project(end_pos).array(), 2)

            pygame.display.flip()
            simulator.apply_forces(1/40.0)
            clock.tick(40)


pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
CLOUD_BASE = 300
GROUND_HEIGHT = 30
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kite Simulator")

GAME_OVER = pygame.USEREVENT + 3

# meters per pixel: image is 34 pixels wide
# a kite is .9 meters. So m/p = .9/34 = .026

# big image is 300 pixes
# m/p = 0.003
projector = Projector(Vector2D(
    SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), .026)

on_string = True
if not on_string:
    initial_pos = Vector2D(0, 3)
else:
    initial_pos = None

# create plane and add to the list of sprites
kite = Kite()
all_sprites = pygame.sprite.Group()
all_sprites.add(kite)

simulator = Simulator()

simulator.register_flying_object(kite.kite)

if on_string:
    pilot = StationaryObject(Vector2D(0, 0))
    simulator.register_stationary_object(pilot, Vector2D(0, 0))
    simulator.tether(
        kite.kite, pilot, kite.kite.bridle_position,
        Vector2D(0, 0), kite.kite.string_length)

    simulator.atmosphere.wind_speed = Vector2D(-5, 0)
else:
    simulator.atmosphere.wind_speed = Vector2D(0, 0)

clouds = pygame.sprite.Group()
explosions = pygame.sprite.Group()

run_game()
pygame.quit()
