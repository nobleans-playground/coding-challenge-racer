#!/usr/bin/env python3


import asyncio

import pygame
import pygame_widgets
from pygame.math import Vector2

import car2
import track1
from linear_math import Transform, Rotation


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
        self.track = Track(track1)
        self.car = car2

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
    def __init__(self, game_state: GameState):
        self.game_state = game_state

        # Create the window, saving it to a variable.
        self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        pygame.display.set_caption("Racer")
        self.font = pygame.font.SysFont(None, 24)

        self.map = self.game_state.track.background.convert()

    def draw(self, game_state: GameState, clock):
        # scale map to full screen
        zoom = self.window.get_width() / self.map.get_width()
        zoom = self.window.get_height() / self.map.get_height() if self.window.get_height() / self.map.get_height() < zoom else zoom
        map_scaled = pygame.transform.scale(self.map, Vector2(self.map.get_size()) * zoom)

        lines = [l * zoom for l in self.game_state.track.lines]
        pygame.draw.aalines(map_scaled, (255, 0, 0), True, lines, 10)

        self.window.blit(map_scaled, (0, 0))

        # Draw the UI
        text = self.font.render(f'fps: {clock.get_fps():.0f}', True, pygame.Color('blue'))
        self.window.blit(text, (20, 20))

        text = self.font.render(
            f'pos: {game_state.position.p.x:.1f} {game_state.position.p.y:.1f} {game_state.position.M.angle:.1f}', True,
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
