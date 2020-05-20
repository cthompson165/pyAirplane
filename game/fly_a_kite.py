import pygame
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from game.kite.box_kite import BoxKite
from game.sprites.explosion import Explosion
from game.enums.colors import Colors
from util.vector_2d import Vector2D
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

        self.pressed_keys = []

        self.kite = BoxKite(.9, .35, .2, .4, .7)
        self.dead = False

        projector.center_x(self.kite.pos())

    def control(self, time):
        self.kite.step(time)

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

        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT or event.type == GAME_OVER:
                running = False

        if not running:
            break

        screen.fill(Colors.SKYBLUE)

        pygame.draw.rect(screen,
                         Colors.FOREST_GREEN,
                         (0, SCREEN_HEIGHT - GROUND_HEIGHT,
                          SCREEN_WIDTH, GROUND_HEIGHT))

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

clouds = pygame.sprite.Group()
explosions = pygame.sprite.Group()

run_game()
pygame.quit()
