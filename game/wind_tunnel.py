import pygame
from pygame.locals import (
    RLEACCEL,
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


class Kite(pygame.sprite.Sprite):

    def __init__(self):
        super(Kite, self).__init__()
        self.original_image = pygame.image.load("game/images/box_kite_big.png")
        self.image = self.original_image
        self.image.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.image.get_rect(
            center=(
                200, 200
            ))

        global atmosphere
        self.kite = SurfacelessKite(
            4, 2, atmosphere,
            kite_position, Angle(0))

        projector.center_x(self.kite.position())

    def update(self):
        position = self.kite.position()
        screen_pos = projector.project(position)
        self.image = pygame.transform.rotate(
            self.original_image, self.kite.orientation().degrees())
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = screen_pos.toint().array()


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

        projected_anchor_position = projector.project(anchor_position)

        pygame.draw.circle(
            screen, Colors.RED,
            projected_anchor_position.toint().array(),
            5, 3)

        if step or not paused:

            kite.update()
            screen.blit(kite.image, kite.rect)

            simulator.add_forces()

            if show_forces:
                debug_draw.draw_forces(kite.kite)

            global_bridle = kite.kite.position().add(
                bridle_position.rotate(
                    kite.kite.orientation()))

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

# meters per pixel: image is 34 pixels wide
# a kite is .9 meters. So m/p = .9/34 = .026

# big image is 300 pixes
# m/p = 0.003
projector = Projector(Vector2D(
    SCREEN_WIDTH, SCREEN_HEIGHT), .0133)

debug_draw = DebugDraw(screen, projector)

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

initial_pos = None

atmosphere = Atmosphere()
kite = Kite()
all_sprites = pygame.sprite.Group()
all_sprites.add(kite)

simulator = Simulator()
simulator.register_flying_object(kite.kite)

bridle_position = Vector2D(1, -1)

anchor = StationaryObject(anchor_position)
simulator.register_stationary_object(anchor, anchor_position)
simulator.tether(
    kite.kite, anchor, bridle_position,
    Vector2D(0, 0), 2)

run_game()
pygame.quit()
