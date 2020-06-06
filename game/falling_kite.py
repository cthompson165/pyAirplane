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
from game.enums.colors import Colors
from util.vector_2d import Vector2D
from projector import Projector
from physics.atmosphere import Atmosphere


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

        self.kite = BoxKite(
            10, .7, .35, .175, .8, .55, Atmosphere(), initial_pos)

        projector.center_x(self.kite.position())

    def update(self):
        position = self.kite.position()

        projector.center(position)

        screen_pos = projector.project(position)

        self.image = pygame.transform.rotate(
            self.original_image, self.kite.orientation().degrees())

        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = screen_pos.toint().array()


def draw_local_point(kite, point):
    world_point = kite.local_to_global(point)
    pygame.draw.circle(
        screen, Colors.BLUE,
        projector.project(world_point).round().array(), 1)


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
                    paused = not paused
                if event.key == K_RIGHT:
                    simulator.atmosphere.wind_speed = \
                        simulator.atmosphere.wind_speed.add(
                            Vector2D(-1, 0))
                if event.key == K_LEFT:
                    simulator.atmosphere.wind_speed = \
                        simulator.atmosphere.wind_speed.add(
                            Vector2D(1, 0))
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

        if step or not paused:
            simulator.add_forces()

            screen.blit(kite.image, kite.rect)

            if show_forces:
                surface_forces = kite.kite.local_forces()
                for force in surface_forces:
                    global_force = force.local_to_global(
                        kite.kite.position(), kite.kite.orientation())
                    start_pos = projector.project(global_force.position)
                    end_pos = projector.project(global_force.endpoint())

                    pygame.draw.line(
                        screen, Colors.RED,
                        start_pos.array(), end_pos.array(), 2)

                airspeed = kite.kite.airspeed()
                position = kite.kite.position()
                end_pos = position.add(airspeed)

                pygame.draw.line(
                    screen, Colors.GREEN,
                    projector.project(position).array(),
                    projector.project(end_pos).array(), 2)

            draw_local_point(kite.kite, kite.kite.front_surface_position)
            draw_local_point(kite.kite, kite.kite.back_surface_position)
            draw_local_point(kite.kite, kite.kite.front_back)
            draw_local_point(kite.kite, kite.kite.back_back)

            pygame.display.flip()

            simulator.apply_forces(1/40)
            kite.update()
            clock.tick(40)


pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kite Simulator")

GAME_OVER = pygame.USEREVENT + 3

# meters per pixel: image is 300 pixels wide
# a kite is .7 meters. So m/p = .7/300 = .00233

# big image is 300 pixels
# m/p = 0.003
projector = Projector(Vector2D(
    SCREEN_WIDTH, SCREEN_HEIGHT), .00233)

on_string = False
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
simulator.atmosphere.wind_speed = Vector2D(0, 0)

run_game()
pygame.quit()
