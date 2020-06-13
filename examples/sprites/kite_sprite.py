import pygame
from pygame.locals import (
    RLEACCEL
)


class KiteSprite(pygame.sprite.Sprite):

    def __init__(self, kite, image_path, projector):
        super(KiteSprite, self).__init__()
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image
        self.image.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.image.get_rect(
            center=(
                200, 200
            ))

        global atmosphere
        self.kite = kite
        self.projector = projector

    def update(self):
        position = self.kite.position()
        screen_pos = self.projector.project(position)
        self.image = pygame.transform.rotate(
            self.original_image, self.kite.orientation().degrees())
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = screen_pos

