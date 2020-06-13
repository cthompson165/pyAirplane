import pygame


class ExplosionSprite(pygame.sprite.Sprite):
    def __init__(self, center, size):

        self._explosion_anim = {}
        self._explosion_anim['lg'] = []
        self._explosion_anim['sm'] = []
        for i in range(9):
            filename = 'examples/images/regularExplosion0{}.png'.format(i)
            img = pygame.image.load(filename).convert()
            img.set_colorkey(pygame.Color("black"))
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
