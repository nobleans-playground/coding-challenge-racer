#!/usr/bin/env python3


import asyncio
from math import degrees

import pygame
from pygame.math import Vector2

from .constants import framerate
from .game_state import GameState
from .linear_math import Transform


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
        zoom = min(self.window.get_width() / self.map.get_width(), self.window.get_height() / self.map.get_height())
        map_scaled = pygame.transform.scale(self.map, Vector2(self.map.get_size()) * zoom)

        lines = [line * zoom for line in self.game_state.track.lines]
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
            self.game_state.update(1 / framerate)

            # Draw the game
            self.clock.tick(framerate)
            self.window.draw(self.clock)
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
