#!/usr/bin/env python3


import asyncio
from math import degrees

import pygame
import pygame_widgets
import racer.car2 as car2
import racer.track1 as track1
from pygame.math import Vector2

from .linear_math import Transform, Rotation


class Track:
    def __init__(self, module):
        self.name: str = module.name
        self.background: pygame.surface.Surface = module.background
        self.lines = [Vector2(l) for l in module.lines]

    def __repr__(self):
        return f"Track({self.name!r}, {self.background!r})"


class GameState:
    def __init__(self):
        self.position = Transform(Rotation.fromangle(0), Vector2(694.59796, 259.5779))
        self.velocity = Vector2()
        self.track = Track(track1)
        self.car = car2

    def update(self, clock: pygame.time.Clock):
        dt = clock.get_time() / 1000
        max_throttle = 100
        max_steering_speed = 3
        slipping_acceleration = 200
        slipping_ratio = 0.6

        keys = pygame.key.get_pressed()
        throttle = 0
        steering_speed = 0
        if keys[pygame.K_LEFT]:
            steering_speed = -max_steering_speed
        if keys[pygame.K_RIGHT]:
            steering_speed = max_steering_speed
        if keys[pygame.K_UP]:
            throttle = max_throttle
        if keys[pygame.K_DOWN]:
            throttle = -max_throttle

        acceleration = self.position.M * Vector2(throttle, 0)

        sideways_velocity = (self.velocity * self.position.M.cols[1]) * self.position.M.cols[1]
        if sideways_velocity.length_squared() > 0.001:
            # slow down the car in sideways direction
            acceleration -= sideways_velocity.normalize() * slipping_acceleration

        # rotate velocity partially
        self.velocity = Rotation.fromangle(steering_speed * dt * (1 - slipping_ratio)) * self.velocity

        # integrate acceleration
        delta_velocity = acceleration * dt
        self.velocity += delta_velocity

        # integrate velocity
        self.position.p += self.velocity * dt
        self.position.M *= Rotation.fromangle(steering_speed * dt)


class Window:
    def __init__(self, game_state: GameState):
        self.game_state = game_state

        # Create the window, saving it to a variable.
        self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        pygame.display.set_caption("Racer")
        self.font = pygame.font.SysFont(None, 24)

        self.map = self.game_state.track.background.convert()

    def draw(self, clock):
        # scale map to full screen
        zoom = self.window.get_width() / self.map.get_width()
        zoom = self.window.get_height() / self.map.get_height() if self.window.get_height() / self.map.get_height() < zoom else zoom
        map_scaled = pygame.transform.scale(self.map, Vector2(self.map.get_size()) * zoom)

        lines = [l * zoom for l in self.game_state.track.lines]
        pygame.draw.aalines(map_scaled, (255, 0, 0), True, lines, 10)

        # Draw the car
        car = self.game_state.car
        car_pos = self.game_state.position.p * zoom
        car_angle = self.game_state.position.M.angle
        car_zoom = car.scale * zoom
        car_image = pygame.transform.rotozoom(car.image, -degrees(car_angle), car_zoom)
        car_rect = car_image.get_rect(center=car_pos)
        map_scaled.blit(car_image, car_rect)

        # Draw the car collision box
        car_footprint = car_zoom * Vector2(car.image.get_size())
        footprint = [car_footprint.elementwise() * v / 2 for v in
                     [Vector2(-1, -1), Vector2(-1, 1), Vector2(1, 1), Vector2(1, -1)]]
        footprint = [Transform(self.game_state.position.M, car_pos) * p for p in footprint]
        pygame.draw.polygon(map_scaled, (0, 255, 0), footprint, 2)

        self.window.blit(map_scaled, (0, 0))

        # Draw the UI
        text = self.font.render(f'fps: {clock.get_fps():.0f}', True, pygame.Color('blue'))
        self.window.blit(text, (20, 20))

        text = self.font.render(
            f'pos: {self.game_state.position.p.x:.1f} {self.game_state.position.p.y:.1f} {self.game_state.position.M.angle:.1f}',
            True,
            pygame.Color('blue'))
        self.window.blit(text, (20, 40))


class App:
    def __init__(self):
        self.game_state = GameState()
        self.window = Window(game_state=self.game_state)
        self.clock = pygame.time.Clock()

    async def mainloop(self):
        run = True
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print('Quitting pygame')
                    pygame.quit()
                    return

            # Update the game
            self.game_state.update(self.clock)

            # Draw the game
            self.clock.tick(60)
            self.window.draw(self.clock)
            pygame_widgets.update(events)
            pygame.display.update()
            await asyncio.sleep(0)  # Very important, and keep it 0


def main():
    pygame.init()
    app = App()
    print('Starting the main loop')
    asyncio.run(app.mainloop())
    print('Main loop finished')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
