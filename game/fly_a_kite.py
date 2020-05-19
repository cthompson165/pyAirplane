''' Run airplane in pygame '''

import random
import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# from aerodynamics.airplanes.seven_four_seven import SevenFourSeven
# from bomber import Bomber
from box_kite import BoxKite
from util.vector_2d import Vector2D
from projector import Projector


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

        self._airplane = BoxKite(
            .9, .4, .28, .35, .8)

        self.dead = False

        self._airplane.debug = False
        self.elevator_percent = 0
        self.throttle_percent = 60

        projector.center(self._airplane.pos())

    def x_velocity(self):
        if self.dead:
            return 0
        else:
            return self._airplane.current_state().vel.x

    def control(self, pressed_keys, joystick, time):

        self._airplane.step(time)

        # print("elevator: " + str(self.elevator_percent))
        # print("throttle: " + str(self.throttle_percent))

    def update(self):
        ''' update the sprite based on plane's state '''
        pos = self._airplane.pos()
        projector.center_x(pos)
        screen_pos = projector.project(pos)

        self.image = pygame.transform.rotate(
            self.original_image, self._airplane.orientation().degrees())

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


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):

        self._explosion_anim = {}
        self._explosion_anim['lg'] = []
        self._explosion_anim['sm'] = []
        for i in range(9):
            filename = 'images/regularExplosion0{}.png'.format(i)
            img = pygame.image.load(filename).convert()
            img.set_colorkey(Colors.BLACK)
            img_lg = pygame.transform.scale(img, (75, 75))
            self._explosion_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img, (32, 32))
            self._explosion_anim['sm'].append(img_sm)

        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = self._explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self._explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self._explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud7.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, CLOUD_BASE),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        velocity = plane.x_velocity() / 50  # divide for parallax
        pixels = projector.get_pixels(velocity)
        self.rect.move_ip(-pixels, 0)
        if self.rect.right < 0:
            self.kill()


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
            elif event.type == ADDCLOUD:

                if not plane.dead:
                    # Create the new cloud and add it to sprite groups
                    new_cloud = Cloud()
                    clouds.add(new_cloud)
                    all_sprites.add(new_cloud)

        if not running:
            break

        screen.fill(Colors.SKYBLUE)

        pygame.draw.rect(screen,
                         Colors.FOREST_GREEN,
                         (0, SCREEN_HEIGHT - GROUND_HEIGHT,
                          SCREEN_WIDTH, GROUND_HEIGHT))

        pressed_keys = pygame.key.get_pressed()

        clouds.update()
        for cloud in clouds:
            screen.blit(cloud.surf, cloud.rect)

        explosions.update()
        for explosion in explosions:
            screen.blit(explosion.image, explosion.rect)

        if not plane.dead:
            plane.control(pressed_keys, joystick, time /
                          1000)  # convert t to seconds
            plane.update()
            screen.blit(plane.image, plane.rect)

        # update the display and clock
        pygame.display.flip()
        time = clock.tick(30)


pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
CLOUD_BASE = 300
GROUND_HEIGHT = 30
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Airplane Simulator")


ADDCLOUD = pygame.USEREVENT + 2
GAME_OVER = pygame.USEREVENT + 3
pygame.time.set_timer(ADDCLOUD, 1000)

pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    print("Using joystick " + joystick.get_name())
    joystick.init()
else:
    print("Using keyboard")

# meters per pixel: image is 250 pixels
# a 747 is 77 meters. So m/p = 77/250 = 308
projector = Projector(Vector2D(SCREEN_WIDTH, SCREEN_HEIGHT), 0.308)

# create plane and add to the list of sprites
plane = Plane()
all_sprites = pygame.sprite.Group()
all_sprites.add(plane)

clouds = pygame.sprite.Group()
explosions = pygame.sprite.Group()

run_game()
pygame.quit()
