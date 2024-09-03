#!/usr/bin/env python3


import asyncio
from math import degrees

import pygame
import pygame_widgets
from pygame import Color
from pygame.math import Vector2
from pygame_widgets.button import Button

from .constants import framerate
from .game_state import GameState
from .linear_math import Transform
from .track import Track
from .tracks import track1


class Window:
    def __init__(self, game_state: GameState):
        self.game_state = game_state

        # Create the window, saving it to a variable.
        self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        pygame.display.set_caption("Racer")
        self.font = pygame.font.SysFont(None, 24)

        self.map = self.game_state.track.background.convert()

        self.reset_button = Button(
            self.window, 20, 20, 80, 30, text='Reset', fontSize=20,
            inactiveColour=(255, 0, 0), hoverColour=(255, 0, 0), pressedColour=(255, 0, 0),
            onClick=lambda: self.game_state.reset()
        )

    def draw(self, clock):
        # scale map to full screen
        zoom = min(self.window.get_width() / self.map.get_width(), self.window.get_height() / self.map.get_height())
        map_scaled = pygame.transform.scale(self.map, Vector2(self.map.get_size()) * zoom)

        lines = [line * zoom for line in self.game_state.track.lines]
        pygame.draw.aalines(map_scaled, (255, 0, 0), True, lines)

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
            # pygame.draw.polygon(map_scaled, bot.color, footprint, 2)

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
        text = self.font.render(f'fps: {clock.get_fps():.0f}', True, pygame.Color('white'))
        self.window.blit(text, (20, 60))

        # Draw each player's name on the right side of the window
        offset_from_top = 20
        # Frist draw a black background
        pygame.draw.rect(self.window, Color('black'),
                         (self.window.get_width() - 300, offset_from_top, 300, len(self.game_state.bots) * 20))

        fastest_bot = self.game_state.ranked()[0]
        for i, bot in enumerate(self.game_state.ranked()):
            car_info = self.game_state.bots[bot]
            fastest_bot_time = self.game_state.bots[fastest_bot].waypoint_timing[len(car_info.waypoint_timing) - 1]
            own_time = car_info.waypoint_timing[len(car_info.waypoint_timing) - 1]
            behind = own_time - fastest_bot_time

            text = self.font.render(f'{bot.name} ({bot.contributor})', True, bot.color)
            self.window.blit(text, (self.window.get_width() - 300, offset_from_top + i * 20))

            # Draw behind time
            text = self.font.render(f'{behind:+.2f}', True, Color('white'))
            self.window.blit(text, (self.window.get_width() - 50, offset_from_top + i * 20))


class App:
    def __init__(self):
        self.game_state = GameState(Track(track1))
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
            pygame_widgets.update(events)
            pygame.display.update()
            await asyncio.sleep(0)  # Very important, and keep it 0
