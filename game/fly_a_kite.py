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
    KEYDOWN,
    QUIT,
)

from aerodynamics.simulator import Simulator
from game.kite.box_kite import BoxKite
from game.sprites.explosion import Explosion
from game.enums.colors import Colors
from util.vector_2d import Vector2D
from projector import Projector
import pymunk


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

        self.kite = BoxKite(10, .9, .35, .2, 1.2, .9)
        self.dead = False

        projector.center_x(self.kite.pos())

    def control(self, time):
        simulator.step(time)  # TODO - move out

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


def run_game():

    clock = pygame.time.Clock()
    running = True
    time = 0

    while running:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT or event.type == GAME_OVER:
                running = False

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            kite.kite.cut_string()
            simulator.atmosphere.wind_speed = Vector2D(0, 0)
        if pressed_keys[K_RIGHT]:
            simulator.atmosphere.wind_speed = \
                    simulator.atmosphere.wind_speed.add(Vector2D(-1, 0))
        if pressed_keys[K_LEFT]:
            simulator.atmosphere.wind_speed = \
                    simulator.atmosphere.wind_speed.add(Vector2D(1, 0))

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

        if not kite.dead:
            kite.control(time / 1000)  # convert t to seconds
            kite.update()
            screen.blit(kite.image, kite.rect)

        # update the display and clock
        pygame.display.flip()
        time = clock.tick(30)


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
projector = Projector(Vector2D(
    SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), .026)

# create plane and add to the list of sprites
kite = Kite()
all_sprites = pygame.sprite.Group()
all_sprites.add(kite)

simulator = Simulator()
simulator.atmosphere.wind_speed = Vector2D(-5, 0)
simulator.register(kite.kite)

pilot = pymunk.Body(body_type=pymunk.Body.STATIC)  # 1
pilot.position = (0, 0)

string = pymunk.SlideJoint(
    kite.kite.body, pilot,
    kite.kite.bridle_position.array(),
    (0, 0), 0,
    kite.kite.string_length)

'''string = pymunk.PinJoint(
    kite.kite.body, pilot,
    kite.kite.bridle_position.array(),
    (0, 0))'''

simulator.register_pymunk(pilot, string)

clouds = pygame.sprite.Group()
explosions = pygame.sprite.Group()

run_game()
pygame.quit()
