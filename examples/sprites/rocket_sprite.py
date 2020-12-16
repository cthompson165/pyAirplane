import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_DOWN
)


class RocketSprite(pygame.sprite.Sprite):
    ''' Plane sprite '''

    ELEVATOR_STEP = 5
    THROTTLE_STEP = 1

    def __init__(self, plane, image_path, projector):
        super(RocketSprite, self).__init__()
        image = pygame.image.load(image_path)
        # back_color = image.get_at((250, 0))

        self.original_image = image
        self.image = image
        self.image.set_colorkey([0, 0, 0], RLEACCEL)
        self.rect = self.image.get_rect(
            center=(
                200, 200
            ))

        self.projector = projector
        self.pressed_keys = []
        self._airplane = plane

        self.dead = False

        self.elevator_percent = 0
        self.throttle_percent = 10

    def x_velocity(self):
        if self.dead:
            return 0
        else:
            return self._airplane.velocity().x

    def _increment_elevator(self):
        self.elevator_percent = min(
            100, self.elevator_percent + RocketSprite.ELEVATOR_STEP)

    def _decrement_elevator(self):
        self.elevator_percent = max(
            -100, self.elevator_percent - RocketSprite.ELEVATOR_STEP)

    def _increment_throttle(self):
        self.throttle_percent = min(
            100, self.throttle_percent + RocketSprite.THROTTLE_STEP)

    def _decrement_throttle(self):
        self.throttle_percent = max(
            0, self.throttle_percent - RocketSprite.THROTTLE_STEP)

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
        self.projector.center(position)
        screen_pos = self.projector.project(position)

        self.image = pygame.transform.rotate(
            self.original_image, self._airplane.orientation().degrees())

        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = screen_pos

    def get_position(self):
        return self._airplane.position()

    def get_joystick_elevator(self, joystick):
        control = joystick.get_axis(1)  # -1 to 1
        elevator_control = -control  # down is up...
        return elevator_control * 100

    def get_joystick_throttle(self, joystick):
        control = joystick.get_axis(2)  # -1 to 1
        control = -control  # it's backward
        throttle_control = (control + 1) / 2.0  # 0 to 1
        return 100 * throttle_control
