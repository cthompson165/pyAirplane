from physics.force import Force
import pygame


class DebugDraw:

    def __init__(self, screen, projector):
        self.colors = {
            Force.LIFT: pygame.Color("blue"),
            Force.DRAG: pygame.Color("dodgerblue"),
            Force.THRUST: pygame.Color("red"),
            Force.GRAVITY: pygame.Color("grey"),
            Force.OTHER: pygame.Color("purple")
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
                    start_pos, end_pos, 2)

        airspeed = flying_object.airspeed()
        position = flying_object.position()
        end_pos = position.add(airspeed)

        pygame.draw.line(
            self.screen, pygame.Color("green"),
            self.projector.project(position),
            self.projector.project(end_pos), 2)
