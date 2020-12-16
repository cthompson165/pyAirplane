import pygame
from pygame.locals import (
    K_ESCAPE,
    K_s,
    K_f,
    K_p,
    KEYDOWN,
    QUIT,
)

from examples.sprites.rocket_sprite import RocketSprite
from examples.sprites.explosion_sprite import ExplosionSprite
from examples.sprites.cloud_sprite import CloudSprite
from flight.simulator import Simulator
from physics.vector_2d import Vector2D
import display
import flight.planes as planes
from flight.atmosphere import Atmosphere


def test_crash():
    if not rocket_sprite.dead:
        if (rocket.position().y - 35) < (GROUND_HEIGHT_METERS - 1):
            rocket_sprite.kill()
            rocket_sprite.dead = True
            expl = ExplosionSprite(projector.project(rocket.position()), 'sm')
            all_sprites.add(expl)
            explosions.add(expl)
            pygame.time.set_timer(GAME_OVER, 1000)
            simulator.unregister(rocket)


def run_game():

    clock = pygame.time.Clock()
    running = True
    paused = False
    show_forces = True

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

                if not rocket_sprite.dead:
                    # Create the new cloud and add it to sprite groups
                    new_cloud = CloudSprite(
                        "examples/images/cloud7.png", SCREEN_WIDTH,
                        CLOUD_BASE_METERS, projector, rocket_sprite, True)

                    clouds.add(new_cloud)
                    all_sprites.add(new_cloud)

        if not running:
            break

        screen.fill(pygame.Color("skyblue"))

        ground_screen_top_left = projector.project(
            Vector2D(0, GROUND_HEIGHT_METERS))

        if projector.is_on_screen(ground_screen_top_left):
            ground_y = ground_screen_top_left[1]
            pygame.draw.rect(screen,
                             pygame.Color("forestgreen"),
                             (0, ground_y,
                              SCREEN_WIDTH, SCREEN_HEIGHT - ground_y))

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

            if not rocket_sprite.dead:
                rocket_sprite.control(pressed_keys, joystick)
                rocket_sprite.update()
                screen.blit(rocket_sprite.image, rocket_sprite.rect)

            if show_forces:
                debug_draw.draw_forces(rocket)

            meters_per_second = rocket.velocity().magnitude()
            km_per_second = meters_per_second / 1000
            km_per_hour = km_per_second * 3600

            seconds = pygame.time.get_ticks() / 1000
            time_text = font.render(
                'Time: ' + str(round(seconds, 2)) + ' seconds',
                False, (0, 0, 0))

            speed_text = font.render(
                'Speed: ' + str(round(km_per_hour, 2)) + ' kph',
                False, (0, 0, 0))

            screen.blit(time_text, (10, 10))
            screen.blit(speed_text, (10, 40))

            pygame.display.flip()
            simulator.apply_forces(1/40.0)
            clock.tick(30)


pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
CLOUD_BASE_METERS = 500
GROUND_HEIGHT_METERS = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Airrocket Simulator")

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

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

# create rocket and add to the list of sprites
atmosphere = Atmosphere()
rocket = planes.FalconHeavy(Vector2D(0, 35), Vector2D(0, 0), atmosphere)

rocket_sprite = RocketSprite(rocket, "examples/images/Falcon_Heavy.png",
                             projector)
all_sprites = pygame.sprite.Group()
all_sprites.add(rocket_sprite)

projector.set_resolution(rocket_sprite.rect.width, 70)
projector.center(rocket.position())
projector.center(rocket.position())

simulator = Simulator()
simulator.register_flying_object(rocket)

clouds = pygame.sprite.Group()
explosions = pygame.sprite.Group()

run_game()
pygame.quit()
