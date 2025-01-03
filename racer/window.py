#!/usr/bin/env python3


import asyncio
import time
from math import degrees

import pygame
import pygame_widgets
from pygame import Color
from pygame.math import Vector2
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

from .constants import framerate, rounds
from .game_state import GameState
from .linear_math import Transform
from .track import Track
from .tracks import all_tracks

starting_track = all_tracks[0]


class Window:
    def __init__(self, game_state, app):
        self.game_state = game_state
        self.app = app

        # Create the window, saving it to a variable.
        self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        pygame.display.set_caption("Racer")
        self.font = pygame.font.SysFont(None, 24)

        self.map = self.game_state.track.background.convert()

        self.reset_button = Button(
            self.window, 20, 20, 80, 30, text='Reset (R)', fontSize=20,
            inactiveColour=(255, 0, 0), hoverColour=(255, 0, 0), pressedColour=(255, 0, 0),
            onClick=lambda: self.game_state.reset()
        )

        self.pause_button = Button(
            self.window, 110, 20, 80, 30, text='Pause (P)', fontSize=20,
            inactiveColour=(255, 0, 0), hoverColour=(255, 0, 0), pressedColour=(255, 0, 0),
            onClick=lambda: self.app.toggle_pause()
        )

        self.step_button = Button(
            self.window, 200, 20, 80, 30, text='Step (S)', fontSize=20,
            inactiveColour=(255, 0, 0), hoverColour=(255, 0, 0), pressedColour=(255, 0, 0),
            onClick=lambda: self.app.do_step()
        )

        self.fast_button = Button(
            self.window, 290, 20, 80, 30, text='Fast (F)', fontSize=20,
            inactiveColour=(255, 0, 0), hoverColour=(255, 0, 0), pressedColour=(255, 0, 0),
            onClick=lambda: self.app.toggle_fast()
        )

        self.present_button = Button(
            self.window, 380, 20, 120, 30, text='Present (off)', fontSize=20,
            inactiveColour=(255, 0, 0), hoverColour=(255, 0, 0), pressedColour=(255, 0, 0),
            onClick=lambda: self.app.toggle_present()
        )

        map_names = [track.name for track in all_tracks]
        self.map_dropdown = Dropdown(
            self.window, 510, 20, 120, 30, name='Switch track',
            choices=map_names, fontSize=20,
            inactiveColour=(255, 0, 0), hoverColour=(255, 0, 0), pressedColour=(255, 0, 0),
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
            if car_info.waypoint_timing:
                fastest_bot_time = self.game_state.bots[fastest_bot].waypoint_timing[len(car_info.waypoint_timing) - 1]
                own_time = car_info.waypoint_timing[len(car_info.waypoint_timing) - 1]
                behind = own_time - fastest_bot_time
            else:
                behind = 0

            text = self.font.render(f'{bot.name} ({bot.contributor})', True, bot.color)
            self.window.blit(text, (self.window.get_width() - 300, offset_from_top + i * 20))

            # Draw behind time
            if car_info.round >= rounds:
                text = self.font.render(f'{car_info.waypoint_timing[-1]:.3f}', True, Color('white'))
            else:
                text = self.font.render(f'{behind:+.3f}', True, Color('white'))
            self.window.blit(text, (self.window.get_width() - 50, offset_from_top + i * 20))

    def selected_track(self):
        name = self.map_dropdown.getSelected()
        if name is None:
            return None
        return next(track for track in all_tracks if track.name == name)

    def reload_track(self):
        self.map = self.game_state.track.background.convert()
        self.map_dropdown.reset()


class App:
    def __init__(self):
        self.paused = False
        self.step = False
        self.fast = False
        self.present = False

        self.game_state = GameState(Track(starting_track))
        self.window = Window(game_state=self.game_state, app=self)
        self.clock = pygame.time.Clock()

    def toggle_pause(self):
        self.paused = not self.paused

    def do_step(self):
        self.step = True

    def toggle_fast(self):
        self.fast = not self.fast

    def toggle_present(self):
        self.present = not self.present
        self.window.present_button.setText(f'Present ({"on" if self.present else "off"})')

    async def mainloop(self):
        run = True
        next_reset = None
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print('Quitting pygame')
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_state.reset()
                    elif event.key == pygame.K_p:
                        self.toggle_pause()
                    elif event.key == pygame.K_s:
                        self.do_step()
                    elif event.key == pygame.K_f:
                        self.toggle_fast()

            if not next_reset and self.present:
                next_reset = time.time() + (60 * 2)
            elif self.present and time.time() > next_reset:
                self.game_state.reset()
                next_reset = None

            if self.window.selected_track() != None and self.window.selected_track() != self.game_state.track:
                print(f'Switching to track {self.window.selected_track().name}')
                self.game_state = GameState(Track(self.window.selected_track()))
                self.window.game_state = self.game_state
                self.window.reload_track()

            if not self.paused or self.step:
                # Update the game
                self.game_state.update(1 / framerate)
                self.step = False

            # Draw the game
            if not self.fast:
                self.clock.tick(framerate)
            self.window.draw(self.clock)
            pygame_widgets.update(events)
            pygame.display.update()
            await asyncio.sleep(0)  # Very important, and keep it 0
