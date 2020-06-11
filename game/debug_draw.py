from physics.force import Force
import pygame


class DebugDraw:

    GREEN = (0, 200, 0)
    BLUE = (0, 0, 128)
    LIGHTBLUE = (0, 0, 255)
    RED = (200, 0, 0)
    GREY = (210, 210, 210)
    PURPLE = (102, 0, 102)

    def __init__(self, screen, projector):
        self.colors = {
            Force.LIFT: DebugDraw.BLUE,
            Force.DRAG: DebugDraw.LIGHTBLUE,
            Force.THRUST: DebugDraw.RED,
            Force.GRAVITY: DebugDraw.GREY,
            Force.OTHER: DebugDraw.PURPLE
        }
        self.projector = projector
        self.screen = screen

    def draw_forces(self, flying_object, force_types=[]):
        surface_forces = flying_object.local_forces()
        for force in surface_forces:
            if force_types is None or len(force_types) == 0 \
                    or force.source in force_types:

                global_force = force.local_to_global(
                    flying_object.position(), flying_object.orientation())
                start_pos = self.projector.project(global_force.position)
                end_pos = self.projector.project(global_force.endpoint())

                pygame.draw.line(
                    self.screen, self.colors[force.source],
                    start_pos.array(), end_pos.array(), 2)

        airspeed = flying_object.airspeed()
        position = flying_object.position()
        end_pos = position.add(airspeed)

        pygame.draw.line(
            self.screen, DebugDraw.GREEN,
            self.projector.project(position).array(),
            self.projector.project(end_pos).array(), 2)
