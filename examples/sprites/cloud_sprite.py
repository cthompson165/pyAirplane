import random
import pygame
from physics.vector_2d import Vector2D
from pygame.locals import (RLEACCEL)


class CloudSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, screen_width,
                 cloud_base_meters, projector, plane_sprite, vertical=False):
        super(CloudSprite, self).__init__()
        self.surf = pygame.image.load(image_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self._cloud_base_meters = cloud_base_meters

        top_left = projector.get_top_left()
        bottom_right = projector.get_bottom_right()

        if vertical:
            x = random.randint(int(top_left.x), int(bottom_right.x))
            self._position = Vector2D(x, int(top_left.y))
        else:
            y = random.randint(int(bottom_right.y), int(top_left.y))
            self._position = Vector2D(int(bottom_right.x), y)

        self._projector = projector
        self.plane_sprite = plane_sprite

        self._screen_pos = self._projector.project(self._position)

        self.rect = self.surf.get_rect(center=self._screen_pos)

    def get_screen_position(self):
        return self._screen_pos

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        if self._position.y <= self._cloud_base_meters:
            self.kill()
        else:
            self._screen_pos = self._projector.project(self._position)
            if not self._projector.is_on_screen(self._screen_pos):
                self.kill()
            else:
                self.rect.center = self._screen_pos
