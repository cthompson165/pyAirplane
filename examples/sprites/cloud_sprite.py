import random
import pygame
from pygame.locals import (RLEACCEL)


class CloudSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, screen_width,
                 cloud_base, projector, plane_sprite):
        super(CloudSprite, self).__init__()
        self.surf = pygame.image.load(image_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, cloud_base),
            )
        )

        self.projector = projector
        self.plane_sprite = plane_sprite

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        velocity = self.plane_sprite.x_velocity() / 50  # divide for parallax
        pixels = self.projector.get_pixels(velocity)
        self.rect.move_ip(-pixels, 0)
        if self.rect.right < 0:
            self.kill()
