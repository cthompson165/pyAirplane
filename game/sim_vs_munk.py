import sys

import pygame
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from projector import Projector
from game.bomber import Bomber
from util.vector_2d import Vector2D
from aerodynamics.simulator_custom import CustomSimulator
from aerodynamics.simulator import Simulator


class Colors:
    ''' colors enum '''
    GREEN = (20, 255, 140)
    FOREST_GREEN = (11, 102, 35)
    GREY = (210, 210, 210)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    PURPLE = (255, 0, 255)
    SKYBLUE = (135, 206, 250)
    BLACK = (0, 0, 0)


class Plane(pygame.sprite.Sprite):
    ''' Plane sprite '''

    ELEVATOR_STEP = 5
    THROTTLE_STEP = 1

    def __init__(self, pos):
        super(Plane, self).__init__()
        self.original_image = pygame.image.load("images/plane4.png")
        self.image = self.original_image
        self.image.set_colorkey([53, 60, 41], RLEACCEL)
        self.rect = self.image.get_rect(
            center=(
                200, 200
            ))

        self.pressed_keys = []

        self._airplane = Bomber(
            pos,
            Vector2D(0, 0))

    def update(self):
        ''' update the sprite based on plane's state '''
        pos = self._airplane.pos()
        screen_pos = projector.project(pos)

        self.image = pygame.transform.rotate(
            self.original_image, self._airplane.orientation().degrees())

        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = screen_pos.toint().array()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
projector = Projector(Vector2D(SCREEN_WIDTH, SCREEN_HEIGHT), 1)

all_sprites = pygame.sprite.Group()

plane = Plane(Vector2D(200, 400))
all_sprites.add(plane)
munk_plane = Plane(Vector2D(600, 400))
all_sprites.add(munk_plane)

simulator = CustomSimulator()
simulator.register(plane._airplane)

munk = Simulator()
munk.register(munk_plane._airplane)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    time = 0

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        # Clear screen
        screen.fill(Colors.SKYBLUE)

        plane.update()
        screen.blit(plane.image, plane.rect)

        munk_plane.update()
        screen.blit(munk_plane.image, munk_plane.rect)

        simulator.step(time / 1000)
        munk.step(time / 1000)

        # update the display and clock
        pygame.display.flip()
        time = clock.tick(30)


if __name__ == '__main__':
    sys.exit(main())
