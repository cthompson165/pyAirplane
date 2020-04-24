import pygame
from airplane import SevenFourSeven
from vector2d import Vector2D
from projector import Projector
import numpy

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class Colors:

  GREEN = (20, 255, 140)
  GREY = (210, 210, 210)
  WHITE = (255, 255, 255)
  RED = (255, 0, 0)
  BLUE = (0, 0, 255)
  PURPLE = (255, 0, 255)
  SKYBLUE = (135, 206, 250)

class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super(Plane, self).__init__()
        self.original_image = pygame.image.load("images/plane4.png")
        self.image = self.original_image
        self.image.set_colorkey([53, 60, 41], RLEACCEL)
        self.rect = self.image.get_rect(
            center=(
                200, 200
            ))

        # meters per pixel: image is 250 pixels
        # a 747 is 77 meters. So m/p = 77/250 = 308
        self._projector = Projector(Vector2D([800, 600]), 0.308)

        self._airplane = SevenFourSeven(Vector2D([5, 5]),
                                        Vector2D([265.3581764, 0]))
        self._airplane._theta = 2.4

    def control(self, pressed_keys, t):
        self.pressed_keys = pressed_keys

        if pressed_keys[K_UP]:
            self._airplane._theta = self._airplane._theta - .01
            print("theta: " + str(self._airplane._theta))
        if pressed_keys[K_DOWN]:
            self._airplane._theta = self._airplane._theta + .01
            print("theta: " + str(self._airplane._theta))

        self._airplane.step(t)

    def update(self):

        self._projector.center(self._airplane.pos())
        screen_pos = self._projector.project(self._airplane.pos())

        self.image = pygame.transform.rotate(self.original_image,
                                             self._airplane.theta())
        self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.center = screen_pos.toint().array()

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

running = True
t = 0
for i in range(1000):

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

    plane.control(pressed_keys, t/1000)
    all_sprites.update()
    screen.blit(plane.image, plane.rect)

    # Refresh Screen
    pygame.display.flip()

    # Number of frames per secong e.g. 60
    t = clock.tick(30)

pygame.quit()