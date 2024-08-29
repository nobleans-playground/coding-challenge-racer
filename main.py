#!/usr/bin/env python3

# Numpy has to be imported first for pygbag
import numpy

assert numpy

import asyncio

import pygame
import pygame_widgets

assert pygame_widgets

from racer.window import App


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
