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
    K_s,
    K_f,
    K_p,
    KEYDOWN,
    QUIT,
)

from aerodynamics.airplanes.seven_four_seven import SevenFourSeven
from aerodynamics.simulator import Simulator
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

    ELEVATOR_STEP = 5
    THROTTLE_STEP = 1

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

        self._airplane = SevenFourSeven(
            Vector2D(5, 5),
            Vector2D(265, 0))

        self.dead = False

        self._airplane.debug = False
        self.elevator_percent = 0
        self.throttle_percent = 60

        projector.center(self._airplane.position())

    def x_velocity(self):
        if self.dead:
            return 0
        else:
            return self._airplane.velocity().x

    def _increment_elevator(self):
        self.elevator_percent = min(
            100, self.elevator_percent + Plane.ELEVATOR_STEP)

    def _decrement_elevator(self):
        self.elevator_percent = max(
            -100, self.elevator_percent - Plane.ELEVATOR_STEP)

    def _increment_throttle(self):
        self.throttle_percent = min(
            100, self.throttle_percent + Plane.THROTTLE_STEP)

    def _decrement_throttle(self):
        self.throttle_percent = max(
            0, self.throttle_percent - Plane.THROTTLE_STEP)

    def control(self, pressed_keys, joystick):

        if joystick is not None:

            self.elevator_percent = self.get_joystick_elevator(joystick)
            self.throttle_percent = self.get_joystick_throttle(joystick)

        else:
            self.pressed_keys = pressed_keys

            if pressed_keys[K_LEFT]:
                self._decrement_throttle()
            elif pressed_keys[K_RIGHT]:
                self._increment_throttle()

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
        self._airplane.set_throttle(self.throttle_percent)

        # print("elevator: " + str(self.elevator_percent))
        # print("throttle: " + str(self.throttle_percent))

    def update(self):
        ''' update the sprite based on plane's state '''
        position = self._airplane.position()
        projector.center_x(position)
        screen_pos = projector.project(position)

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
            simulator.unregister(plane._airplane)

    def get_joystick_elevator(self, joystick):
        control = joystick.get_axis(1)  # -1 to 1
        elevator_control = -control  # down is up...
        return elevator_control * 100

    def get_joystick_throttle(self, joystick):
        control = joystick.get_axis(2)  # -1 to 1
        control = -control  # it's backward
        throttle_control = (control + 1) / 2.0  # 0 to 1
        return 100 * throttle_control


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
    paused = False
    show_forces = False

    while running:
        step = False
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_s:
                    step = True
                if event.key == K_p:
                    paused = not paused
                if event.key == K_f:
                    show_forces = not show_forces
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

        if step or not paused:

            simulator.add_forces()

            clouds.update()
            for cloud in clouds:
                screen.blit(cloud.surf, cloud.rect)

            explosions.update()
            for explosion in explosions:
                screen.blit(explosion.image, explosion.rect)

            if not plane.dead:
                plane.control(pressed_keys, joystick)
                plane.update()
                screen.blit(plane.image, plane.rect)

            if show_forces:
                surface_forces = plane._airplane.local_forces()
                for force in surface_forces:
                    if "engine" not in force.name:
                        global_force = force.local_to_global(
                            plane._airplane.position(),
                            plane._airplane.orientation())
                        start_pos = projector.project(global_force.position)
                        end_pos = projector.project(global_force.endpoint())

                        pygame.draw.line(
                            screen, Colors.RED,
                            start_pos.array(), end_pos.array(), 2)

            pygame.display.flip()
            simulator.apply_forces(1/40.0)
            clock.tick(30)


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

simulator = Simulator()
simulator.register_flying_object(plane._airplane)

clouds = pygame.sprite.Group()
explosions = pygame.sprite.Group()

run_game()
pygame.quit()
