#!/usr/bin/env python3


import asyncio
from argparse import Namespace
from copy import deepcopy
from math import degrees

import pygame
import pygame_widgets
import racer.car1 as car1
import racer.track1 as track1
from pygame.math import Vector2

from .bots import all_bots
from .car_info import CarInfo
from .linear_math import Transform


class Track:
    def __init__(self, module):
        self.name: str = module.name
        self.background: pygame.surface.Surface = module.background
        self.track_width: float = module.track_width
        self.lines = [Vector2(l) for l in module.lines]

    def __deepcopy__(self, memo):
        return Track(Namespace(name=deepcopy(self.name),
                               background=self.background.copy(),
                               track_width=deepcopy(self.track_width),
                               lines=deepcopy(self.lines)))

    def __repr__(self):
        return f"Track({self.name!r}, {self.background!r})"


class GameState:
    def __init__(self):
        self.track = Track(track1)
        self.bots = {}
        for Bot in all_bots:
            self.bots[Bot(deepcopy(self.track))] = CarInfo(car1, self.track)

    def update(self, clock: pygame.time.Clock):
        # keys = pygame.key.get_pressed()
        # throttle = 0
        # steering_command = 0
        # if keys[pygame.K_LEFT]:
        #     steering_command = -1
        # if keys[pygame.K_RIGHT]:
        #     steering_command = 1
        # if keys[pygame.K_UP]:
        #     throttle = 1
        # if keys[pygame.K_DOWN]:
        #     throttle = -1
        for bot, car_info in self.bots.items():
            result = bot.compute_commands(car_info.next_waypoint, deepcopy(car_info.position),
                                          deepcopy(car_info.velocity))
            if type(result) is tuple:
                throttle, steering_command = result
            else:
                print(f"Bot {bot.name} returned {type(result)} instead of a Tuple")
                throttle, steering_command = 0, 0
            car_info.update(clock.get_time() / 1000, throttle, steering_command)


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

        # Draw the cars
        for bot, car_model in self.game_state.bots.items():
            car_pos = car_model.position.p * zoom
            car_angle = car_model.position.M.angle
            car_zoom = car_model.car_type.scale * zoom
            car_image = pygame.transform.rotozoom(car_model.car_type.image, -degrees(car_angle), car_zoom)
            car_rect = car_image.get_rect(center=car_pos)
            map_scaled.blit(car_image, car_rect)

            # Draw the car collision box
            car_footprint = car_zoom * Vector2(car_model.car_type.image.get_size())
            footprint = [car_footprint.elementwise() * v / 2 for v in
                         [Vector2(-1, -1), Vector2(-1, 1), Vector2(1, 1), Vector2(1, -1)]]
            footprint = [Transform(car_model.position.M, car_pos) * p for p in footprint]
            pygame.draw.polygon(map_scaled, bot.color, footprint, 2)

            # Draw a line from the car to the next waypoint
            next_waypoint_scaled = self.game_state.track.lines[car_model.next_waypoint] * zoom
            pygame.draw.line(map_scaled, bot.color, car_pos, next_waypoint_scaled, 2)

            # Draw a circle with the track width at the next waypoint
            pygame.draw.circle(map_scaled, bot.color, next_waypoint_scaled,
                               int(self.game_state.track.track_width * zoom), 2)

            # Draw the car's name
            text = self.font.render(f'{bot.name}', True, bot.color)
            map_scaled.blit(text, (car_pos.x - 50, car_pos.y - 50))

            # Draw debug info
            bot.draw(map_scaled, zoom)

        self.window.blit(map_scaled, (0, 0))

        # Draw the UI
        text = self.font.render(f'fps: {clock.get_fps():.0f}', True, pygame.Color('blue'))
        self.window.blit(text, (20, 20))

        text = self.font.render(
            f'pos: {car_model.position.p.x:.1f} {car_model.position.p.y:.1f} {car_model.position.M.angle:.1f}',
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
