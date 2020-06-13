import pygame
from pygame.locals import (
    K_ESCAPE,
    K_s,
    K_f,
    K_p,
    KEYDOWN,
    QUIT,
)

from examples.sprites.plane_sprite import PlaneSprite
from examples.sprites.explosion_sprite import ExplosionSprite
from examples.sprites.cloud_sprite import CloudSprite
from flight.simulator import Simulator
from physics.vector_2d import Vector2D
import display
import flight.planes as planes


def test_crash():
    if not plane_sprite.dead:
        screen_pos = projector.project(plane.position())
        if (screen_pos[1] >= (SCREEN_HEIGHT - GROUND_HEIGHT - 20)):
            plane_sprite.kill()
            plane_sprite.dead = True
            expl = ExplosionSprite(screen_pos, 'sm')
            all_sprites.add(expl)
            explosions.add(expl)
            pygame.time.set_timer(GAME_OVER, 1000)
            simulator.unregister(plane)


def run_game():

    clock = pygame.time.Clock()
    running = True
    paused = False
    show_forces = False

    while running:
        step = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_s:
                    step = True
                if event.key == K_p:
                    paused = not paused
                if event.key == K_f:
                    show_forces = not show_forces
            elif event.type == QUIT or event.type == GAME_OVER:
                running = False
            elif event.type == ADDCLOUD:

                if not plane_sprite.dead:
                    # Create the new cloud and add it to sprite groups
                    new_cloud = CloudSprite(
                        "examples/images/cloud7.png", SCREEN_WIDTH,
                        CLOUD_BASE, projector, plane_sprite)

                    clouds.add(new_cloud)
                    all_sprites.add(new_cloud)

        if not running:
            break

        screen.fill(pygame.Color("skyblue"))

        pygame.draw.rect(screen,
                         pygame.Color("forestgreen"),
                         (0, SCREEN_HEIGHT - GROUND_HEIGHT,
                          SCREEN_WIDTH, GROUND_HEIGHT))

        pressed_keys = pygame.key.get_pressed()

        if step or not paused:

            test_crash()

            simulator.add_forces()

            clouds.update()
            for cloud in clouds:
                screen.blit(cloud.surf, cloud.rect)

            explosions.update()
            for explosion in explosions:
                screen.blit(explosion.image, explosion.rect)

            if not plane_sprite.dead:
                plane_sprite.control(pressed_keys, joystick)
                plane_sprite.update()
                screen.blit(plane_sprite.image, plane_sprite.rect)

            if show_forces:
                debug_draw.draw_forces(plane)

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

projector = display.Projector(Vector2D(SCREEN_WIDTH, SCREEN_HEIGHT))
debug_draw = display.DebugDraw(screen, projector)

# create plane and add to the list of sprites
plane = planes.SevenFourSeven(Vector2D(5, 14000), Vector2D(265, 0))

plane_sprite = PlaneSprite(plane, "examples/images/plane4.png", projector)
all_sprites = pygame.sprite.Group()
all_sprites.add(plane_sprite)

projector.set_resolution(plane_sprite.rect.width, 77)
projector.center(plane.position())

simulator = Simulator()
simulator.register_flying_object(plane)

clouds = pygame.sprite.Group()
explosions = pygame.sprite.Group()

run_game()
pygame.quit()
