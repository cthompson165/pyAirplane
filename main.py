''' Run airplane in pygame '''

import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from aerodynamics.airplanes.seven_four_seven import SevenFourSeven
from util.vector_2d import Vector2D
from util.projector import Projector


class Colors:
    ''' colors enum '''
    GREEN = (20, 255, 140)
    GREY = (210, 210, 210)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    PURPLE = (255, 0, 255)
    SKYBLUE = (135, 206, 250)


class Plane(pygame.sprite.Sprite):
    ''' Plane sprite '''

    ELEVATOR_STEP = 5

    def __init__(self):
        super(Plane, self).__init__()
        self.original_image = pygame.image.load("images/plane4.png")
        self.image = self.original_image
        self.image.set_colorkey([53, 60, 41], RLEACCEL)
        self.rect = self.image.get_rect(
            center=(
                200, 200
            ))

        self.pressed_keys = []

        # meters per pixel: image is 250 pixels
        # a 747 is 77 meters. So m/p = 77/250 = 308
        self._projector = Projector(Vector2D(800, 600), 0.308)

        self._airplane = SevenFourSeven(Vector2D(5, 5),
                                        Vector2D(265, 0))

        self._airplane.debug = False
        self.elevator_percent = 0

        self._projector.center(self._airplane.pos())

    def _increment_elevator(self):
        self.elevator_percent = min(
            100, self.elevator_percent + Plane.ELEVATOR_STEP)

    def _decrement_elevator(self):
        self.elevator_percent = max(
            -100, self.elevator_percent - Plane.ELEVATOR_STEP)

    def control(self, pressed_keys, time):
        ''' pass user control input to the plane '''
        self.pressed_keys = pressed_keys

        if pressed_keys[K_UP]:
            self._increment_elevator()
        elif pressed_keys[K_DOWN]:
            self._decrement_elevator()
        else:
            if self.elevator_percent < 0:
                self._increment_elevator()
            elif self.elevator_percent > 0:
                self._decrement_elevator()

        self._airplane.apply_pitch_control(self.elevator_percent)

        self._airplane.step(time)

    def update(self):
        ''' update the sprite based on plane's state '''
        pos = self._airplane.pos()
        self._projector.center_x(pos)
        screen_pos = self._projector.project(pos)

        self.image = pygame.transform.rotate(
            self.original_image, self._airplane.orientation().degrees())

        self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.center = screen_pos.toint().array()


def run():
    ''' run the game '''
    running = True
    time = 0
    while running:

        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

        if not running:
            break

        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()

        # Drawing on Screen
        screen.fill(Colors.SKYBLUE)

        plane.control(pressed_keys, time/1000)  # convert t to seconds
        all_sprites.update()
        screen.blit(plane.image, plane.rect)

        # Refresh Screen
        pygame.display.flip()

        # Number of frames per secong e.g. 60

        time = clock.tick(30)


pygame.init()

SCREENWIDTH = 800
SCREENHEIGHT = 600

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Airplane Simulator")

# create plane and add to the list of sprites
plane = Plane()
all_sprites = pygame.sprite.Group()
all_sprites.add(plane)

clock = pygame.time.Clock()
run()
pygame.quit()
