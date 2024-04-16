#!/usr/bin/env python3


import asyncio
from math import degrees

import pygame
import pygame_widgets
from pygame import Rect
from pygame.math import Vector2
from pygame_widgets.dropdown import Dropdown

import car
import track1
from linear_math import Transform, Rotation
from track import Track


class GameState:
    def __init__(self):
        self.position = Transform(Rotation.fromangle(0), Vector2(694.59796, 259.5779))
        self.track = Track(track1)
        self.car = car

    def update(self):
        keys = pygame.key.get_pressed()
        forward = 0.1
        angle = 0.05
        delta = Transform()
        if keys[pygame.K_LEFT]:
            delta.M = Rotation.fromangle(angle)
        if keys[pygame.K_RIGHT]:
            delta.M = Rotation.fromangle(-angle)
        if keys[pygame.K_UP]:
            delta.p.x = forward
        if keys[pygame.K_DOWN]:
            delta.p.x = -forward
        self.position = self.position * delta


class Window:
    def __init__(self):
        # Create the window, saving it to a variable.
        self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        pygame.display.set_caption("Example resizable window")
        self.font = pygame.font.SysFont(None, 24)

        self.car_image = pygame.image.load("car.png").convert_alpha()
        # self.car_image = pygame.transform.scale(self.car_image, (100, 200))

        self.camera_pos = Transform()  # meters
        self.camera_resolution: float = float('nan')  # pixel/m

        self.camera_dropdown = Dropdown(
            self.window, 0, 0, 100, 50,
            name='Select camera view',
            choices=['Fullscreen', 'Zoom', 'Player1']
        )
        self.camera_dropdown.chosen = self.camera_dropdown._Dropdown__choices[0]

    def draw(self, game_state: GameState, clock):
        self.window.fill((0, 0, 0))

        viewport_rect = Rect(50, 50, self.window.get_width() - 200, self.window.get_height() - 100)
        viewport = self.window.subsurface(viewport_rect)
        viewport.fill((40, 0, 0))

        # width, height = self.window.get_size()
        if self.camera_dropdown.getSelected() == 'Fullscreen':
            self.camera_pos.p = Vector2(0, 0)
            self.camera_resolution = viewport.get_width() / game_state.track.size.x
        elif self.camera_dropdown.getSelected() == 'Zoom':
            x, y = pygame.mouse.get_pos()
            self.camera_pos.p = Vector2(x, viewport.get_height() - y)
            self.camera_pos.p.x /= viewport.get_width()
            self.camera_pos.p.y /= viewport.get_height()
            self.camera_pos.p.x *= game_state.track.size.x
            self.camera_pos.p.y *= game_state.track.size.y
            self.camera_resolution = 5
        else:
            raise NotImplementedError(self.camera_dropdown.getSelected())

        # Draw the track
        # First, convert the track to the camera space
        map_to_camera = self.camera_pos.inverse()
        track_lines = [map_to_camera * p for p in game_state.track.lines]
        # fix lines resolution
        track_lines = [p * self.camera_resolution for p in track_lines]
        # to draw a line, the y axis is inverted
        track_lines = [Vector2(p.x, viewport.get_height() - p.y) for p in track_lines]
        track_width = game_state.track.width * self.camera_resolution

        pygame.draw.lines(viewport, (255, 255, 255), True, track_lines, int(track_width))

        # Draw the car
        # car_rotated, car_rect = rotate_image_around_point(self.car_image, degrees(game_state.position.M.angle) - 90,
        #                                                   self.car_image.get_width() / 2,
        #                                                   self.car_image.get_height() / 2)
        # car_rect.move_ip(Vector2(self.car_image.get_size()) / -2)
        # car_pos = map_to_camera * game_state.position.p
        # car_pos = car_pos * self.camera_resolution
        # car_pos = Vector2(car_pos.x, self.window.get_height() - car_pos.y)
        # car_rect.move_ip(car_pos.x, car_pos.y)

        car_length = car.footprint.x / 2 * self.camera_resolution  # in pixels
        car_scale = car_length / self.car_image.get_width()
        car_rotated = pygame.transform.rotozoom(self.car_image, degrees(game_state.position.M.angle) - 90, car_scale)

        car_pos = map_to_camera * game_state.position.p
        car_pos = car_pos * self.camera_resolution
        car_pos.y = viewport.get_height() - car_pos.y  # flip y

        car_rect = car_rotated.get_rect()
        car_rect.center = (0, 0)
        # car_rect.move_ip(Vector2(self.car_image.get_size()) / -2 * car_scale)
        # import ipdb; ipdb.set_trace()
        car_rect.move_ip(car_pos.x, car_pos.y)

        viewport.blit(car_rotated, car_rect)

        footprint = game_state.car.footprint
        footprint_lines = [(footprint.x / 2, footprint.y / 2), (footprint.x / 2, footprint.y / -2),
                           (footprint.x / -2, footprint.y / -2), (footprint.x / -2, footprint.y / 2)]
        footprint_lines = [game_state.position * Vector2(point) for point in footprint_lines]
        footprint_lines = [map_to_camera * point for point in footprint_lines]
        footprint_lines = [self.camera_resolution * point for point in footprint_lines]
        # to draw a line, the y axis is inverted
        footprint_lines = [Vector2(p.x, viewport.get_height() - p.y) for p in footprint_lines]
        pygame.draw.lines(viewport, (0, 255, 0), True, footprint_lines)

        # Draw a car
        # car_surface = pygame.Surface([100, 200], pygame.SRCALPHA)
        # car_surface.fill((0, 0, 0))
        # car_surface.blit(self.car_image, (0, 0))
        # text = self.font.render('player1', True, pygame.Color('yellow'))
        # car_surface.blit(text, (20, 20))

        # car_rotated = pygame.transform.rotate(car_surface, degrees(game_state.position.M.angle) - 90)
        # car_rect = car_rotated.get_rect(
        #     center=(game_state.position.p.x, self.window.get_height() - game_state.position.p.y))
        # self.window.blit(car_rotated, (car_rect.x, car_rect.y))

        # Draw the UI
        text = self.font.render(f'fps: {clock.get_fps():.0f}', True, pygame.Color('blue'))
        self.window.blit(text, (20, 20))

        text = self.font.render(
            f'pos: {game_state.position.p.x:.1f} {game_state.position.p.y:.1f} {game_state.position.M.angle:.1f}', True,
            pygame.Color('blue'))
        self.window.blit(text, (20, 40))

        text = self.font.render(
            f'camera: {self.camera_pos.p.x:.1f} {self.camera_pos.p.y:.1f} {self.camera_pos.M.angle:.1f}', True,
            pygame.Color('blue'))
        self.window.blit(text, (20, 60))

        self.camera_dropdown.setX(self.window.get_width() - 200)


def rotate_image_around_point(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect


class App:
    def __init__(self):
        self.window = Window()
        self.game_state = GameState()
        self.clock = pygame.time.Clock()

    async def mainloop(self):
        run = True
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print('Quitting pygame')
                    pygame.quit()
                    return

            # Update the game
            self.game_state.update()

            # Draw the game
            self.clock.tick(60)
            self.window.draw(self.game_state, self.clock)
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
